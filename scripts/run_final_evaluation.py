# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.  
# SPDX-License-Identifier: CC-BY-NC-4.0

from argparse import ArgumentParser
import json
import os
import re
from functools import partial

from tqdm import tqdm
import numpy as np
import getpass
from langchain_huggingface import HuggingFaceEmbeddings

from dstc12.eval import (
    acc,
    nmi,
    rouge_with_multiple_references,
    cosine_similarity_with_multiple_references,
    bertscore_with_multiple_references,
)
from bedrock_inferencer import BedrockInferencer
from prompts.styleguide_full import GENERIC_PROMPT, SECTION_1_RULES, SECTION_2_RULES


class StyleguideEvaluator(BedrockInferencer):
    def __init__(self, prompt_template):
        super().__init__(self)
        self.prompt = prompt_template

    def build_prompt(self, theme_label=''):
        return self.prompt(theme_label=theme_label)

    def process_prediction(self, output):
        score_pattern = r'<score>(.*?)</score>'
        score = re.search(score_pattern, output, re.DOTALL).group(1).strip() if score_pattern else None
        exp_pattern = r'<explanation>(.*?)</explanation>'
        explanation = re.search(exp_pattern, output, re.DOTALL).group(1).strip() if exp_pattern else None
        return output, int(score.lower() == 'good'), explanation


def run_non_llm_eval(references, predictions, embedding_model_name):
    label_1_references, label_2_references = references
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    reference_1_embeddings = embeddings.embed_documents(label_1_references)
    reference_2_embeddings = embeddings.embed_documents(label_2_references)
    predictions_embeddings = embeddings.embed_documents(predictions)

    avg_acc = acc(references=label_1_references, predictions=predictions)
    avg_nmi = nmi(references=label_1_references, predictions=predictions)
    avg_rouge = rouge_with_multiple_references(
        [[label_1, label_2] for label_1, label_2 in zip(label_1_references, label_2_references)],
        predictions
    )
    avg_cosine_similarity = cosine_similarity_with_multiple_references(
        (reference_1_embeddings, reference_2_embeddings),
        predictions_embeddings
    )
    avg_bertscore = bertscore_with_multiple_references(
         [[label_1, label_2] for label_1, label_2 in zip(label_1_references, label_2_references)],
        predictions
    )

    return {
        'acc': float(avg_acc),
        'nmi': float(avg_nmi),
        'rouge_1': float(avg_rouge['rouge1'].fmeasure),
        'rouge_2': float(avg_rouge['rouge2'].fmeasure),
        'rouge_l': float(avg_rouge['rougeL'].fmeasure),
        'cosine_similarity': float(avg_cosine_similarity),
        'bertscore_p': float(avg_bertscore['bertscore_p']),
        'bertscore_r': float(avg_bertscore['bertscore_r']),
        'bertscore_f1': float(avg_bertscore['bertscore_f1']),
    }


def run_llm_eval(predictions):
    section_judges = [
        StyleguideEvaluator(partial(GENERIC_PROMPT.format, rules_content=section))
        for section in [SECTION_1_RULES, SECTION_2_RULES]
    ]
    judgements = []
    for pred in tqdm(predictions):
        judgement = {}
        for section_name, section_judge in zip(['section_1', 'section_2'], section_judges):
            raw_llm_output, score, explanation = section_judge.get_inference_results_regex(theme_label=pred)
            judgement[section_name] = {
                'raw_llm_output': raw_llm_output,
                'score': score,
                'explanation': explanation,
            }
        judgements.append(judgement)
    section_1_score = float(np.mean([judgement['section_1']['score'] for judgement in judgements]))
    section_2_score = float(np.mean([judgement['section_2']['score'] for judgement in judgements]))
    return {
        'llmaaj_section_1': section_1_score,
        'llmaaj_section_2': section_2_score,
        'llmaaj_avg': float(np.mean([section_1_score, section_2_score])),
        'llmaaj_outputs': judgements
    }


def main(references, predictions, embedding_model_name):
    non_llm_metrics = run_non_llm_eval(references, predictions, embedding_model_name)
    llm_metrics = run_llm_eval(predictions)
    return non_llm_metrics | llm_metrics


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('predictions_file', type=str)
    parser.add_argument('ground_truth_file', type=str)
    parser.add_argument('output_file', type=str)
    parser.add_argument('--embedding-model-name', type=str, default='sentence-transformers/all-mpnet-base-v2')
    parser.add_argument('--llm-eval', action='store_true', default=False)
    parser.add_argument('--non-llm-eval', action='store_true', default=False)
    args = parser.parse_args()
    if not args.llm_eval and not args.non_llm_eval:
        parser.error("At least one of --llm-eval or --non-llm-eval must be set")
    return args


if __name__ == '__main__':
    args = parse_args()

    with open(args.ground_truth_file) as f:
        ground_truth = [json.loads(line) for line in f]
    with open(args.predictions_file) as f:
        predictions = [json.loads(line) for line in f]

    assert len(ground_truth) == len(predictions)

    label1_references, label2_references, label_predictions = [], [], []
    for dialog_gt, dialog_pred in zip(ground_truth, predictions):
        assert len(dialog_gt['turns']) == len(dialog_pred['turns'])
        for utterance_gt, utterance_pred in zip(dialog_gt['turns'], dialog_pred['turns']):
            assert utterance_gt['utterance_id'] == utterance_pred['utterance_id']
            if utterance_gt['theme_label'] is None:
                continue
            uid = utterance_gt['utterance_id']
            label1_references.append(utterance_gt['theme_label']['label_1'])
            label2_references.append(utterance_gt['theme_label']['label_2'])
            label_predictions.append(utterance_pred['theme_label_predicted'])
    result = {}
    if args.non_llm_eval:
        result |= run_non_llm_eval((label1_references, label2_references), label_predictions, args.embedding_model_name)
        with open(args.output_file, 'w') as f_out:
            print(json.dumps(result), file=f_out)
    if args.llm_eval:
        llmaaj_result = run_llm_eval(label_predictions)
        result |= llmaaj_result
        with open(args.output_file, 'w') as f_out:
            print(json.dumps(result), file=f_out)


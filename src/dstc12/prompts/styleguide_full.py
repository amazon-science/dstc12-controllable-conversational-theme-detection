# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.  
# SPDX-License-Identifier: CC-BY-NC-4.0


GENERIC_PROMPT = \
'''You are a useful and intelligent judge evaluating a theme label, a short, concise and useful textual description of a conversation at a callcenter.
Your task is to read the theme label guideline carefully and evaluate a theme label against it.



Theme Label Writing Guideline

An acceptable theme label satisfies two families of criteria:

1. Structural criteria relate to the linguistic structure of the theme label, including its syntax and morphology, as well as its style and conciseness. A theme label that meets the formal criteria is said to be structurally well formed.
2. Semantico-pragmatic criteria relate to the linguistic meaning of the theme label, including its reference (what it refers to), its generality, and its usability. A theme label that meets these criteria is said to be semantico-pragmatically well formed.

<rules>
{rules_content}
</rules>

Your task if the following: output Good if the theme label within <theme_label></theme_label> tags fully conforms to the rules within <rules></rules> tags, Bad otherwise.
Use the following format:

<explanation>put here all the subsections that this label violated, or "All good" otherwise</explanation>
<score>Good / Bad</score>

<theme_label>
{theme_label}
</theme_label>

'''

SECTION_1_RULES = \
'''1. Structural criteria

All of the following statements are true of structurally well-formed theme labels.

1A - The theme label is a bare verb phrase.

For our purposes, the term verb phrase refers to the chunk of a sentence that contains the verb and any of its arguments or modifiers. A verb phrase describes an event. Most arguments or modifiers will be either a direct object (the entity that is acted upon in an event), an indirect object (the recipient of the direct object in an event), or a prepositional phrase (a preposition followed by a noun phrase that modifies the meaning of the verb phrase in some way).

A bare verb phrase includes a verb in its bare form. The bare form of a verb does not include any tense or agreement; it is the form that would normally follow the infinitive to, such as “sign up” in “I’d like to sign up”. It is the citation form of the verb (the form you would look for in a dictionary).

<examples>
<example>
Good: sign up for membership
Bad: signing up for membership
Explanation: This is a verb phrase, but the verb is not in the bare form; it is morphologically complex. Aspect markers like -ing should not be included in theme labels.

Bad: membership sign-up
Explanation: This is a noun phrase.	
</example>

<example>
Good: request late check-in
Bad: requested late check-in
Explanation: This is a verb phrase, but the verb is in the past tense form.

Bad: request for late check-in
Explanation: This is a noun phrase. (Did you get my request for a late check-in?)

Bad: late check-in
Explanation: This is a noun phrase in which the main noun (check-in) is being modified by an adjective (late).
</example>
<example>
Good: rent vehicles
Bad: will rent vehicle
Explanation: This is a verb phrase, but the verb is not bare. The future tense modal will should not be included in theme labels.
Bad: vehicle rentals
Explanation: This is a (plural) noun phrase.
Bad: rental of vehicles
Explanation: This is a noun phrase.
Bad: renting vehicles
Explanation: This is a verb phrase, but the verb is not in the bare form. Aspect markers like -ing should not be included in theme labels.
</example>
<example>
Good: redeem store credit
Bad: to redeem store credit
Explanation: Although the verb is in its bare form, the infinitive marker to should never be included in theme labels.
Bad: redemption of store credit
Explanation: This is a noun phrase.
Bad: store credit redemption
Explanation: This is a noun phrase.
</example>

<example>
Good: open account
Bad: new account
Explanation: This is a noun phrase.
</example>
</examples>

1B - The theme label is concise and telegraphic.

Theme labels should be concise, at approximately 2-5 words. They should also be written in a telegraphic style, similar to the style of newspaper headlines, which must be short in order to preserve space and ink. For our purposes, telegraphic theme labels (a) primarily contain content words (i.e. open-class words), and (b) exclude most function words (i.e. closed-class words).

Types of content (open-class) words:
nouns (items, insurance, information, order, etc.)
main (non-auxiliary) verbs (check, inquire, add, explore, etc.)
adjectives (new patient, missing item, etc.)
other categories serving as modifiers (shipping information, product options, etc.)

Types of function (closed-class) words:
articles/determiners (the, a, etc.)
auxiliary verbs (any form of have, or be)
copulas (be when it doesn't precede another verb, seem, etc.)
negation (not or -n't)
conjunctions (and, or, but, etc.)
complementizers (clause-embedding uses of that, for, if, or whether)
modals (can, could, will, would, may, might, must, shall)
question words (who, what, where, when, how, why)

<examples>
<example>
Good: sign up for membership  
Bad: sign up for a membership  
Explanation: This includes an unneeded function word (the article a).  
</example>

<example>
Good: request late check-in  
Bad: ask if late check-in possible  
Explanation: Although this is a verb phrase, it includes a function word (if) that would not be needed if a more efficient wording was selected.  
</example>

<example>
Good: redeem store credit  
Bad: try to redeem store credit  
Explanation: Though this fits within the word limit, a simpler alternative with essentially the same meaning should always be chosen (if available).  

Bad: use store credit instead of card  
Explanation: Too long (6 words)
</example>

Bad: don't use credit card  
Explanation: Includes negation
<example>

<example>
Good: open account  
Bad: have account opened  
Explanation: Although this is a verb phrase, it is unnecessarily convoluted. The simpler alternative *open account* would always be preferred.  

Bad: open up account  
Explanation: Informally, *open up* is perfectly natural, but *open account* should be chosen instead since it contains fewer words.  
</example>
</examples>'''

SECTION_2_RULES = \
'''2. Semantico-pragmatic criteria

2A - The theme label is eventive.

Theme labels should only describe a class of events. Events refer to something that can be said to happen, and they are differentiated from (a) states (a condition or state of existence, e.g. states of need or desire), (b) entities (an object or thing that exists, or a class of objects or things that exist), (c) properties (a characteristic that can be attributed to entities), and (d) propositions (statements, which can be judged as true or false in a specific situation).

Some of the following unacceptable examples already do not satisfy structural criterion 1A, but all of them are already constructed to satisfy 1B.

Acceptable theme labels:
Events
cancel booking
cancel hotel reservation
get warranty replacement
request warranty relacement
report defective product

Unacceptable theme labels
States
want to cancel booking
has to replace product
believe product is defective

Properties
want to cancel booking;
need to cancel room
hope to get warranty replacement;
angry about defective product
product defect

Entities/Entity types
booking cancellation;
cancellation of reservation
warranty replacement
defective product

Propositions
customer wants to cancel booking;
customer cancels booking
customer needs warranty replacement
product is defective

2B - The theme label is actionable.

Theme labels should be able to be used to identify a series of standard resolution steps (steps to resolve the problem that drove the customer to make contact) for a customer intent that the theme label classifies. Non-actionable theme labels may be excessively vague or require broad follow-up questions such as “How can I help you with that?” in order to understand a customer issue that the theme label classifies. 

Theme labels that violate 2B will often (but not necessarily) also violate 1A.

<examples>
<example>
Good: schedule appointment  
Bad: appointments  
Explanation: This theme label doesn't inform what is to be done with an appointment (cancel? schedule? reschedule?), so it is not actionable.  
</example>

<example>
Good: add user  
Bad: new person  
Explanation: The phrase *new person* is too vague and does not specify the action of adding a user.  
</example>

<example>
Good: dispute charge  
Bad: complain about something  
Explanation: This is likely too vague to be actionable.  
</example>

<example>
Good: get information about loan options  
Bad: loan options  
Explanation: This theme label lacks an actionable verb, making it unclear whether the intent is to apply, compare, or inquire about loans.  
</example>

<example>
Good: track order  
Bad: track  
Explanation: The theme label is too vague and does not specify what is being tracked.  
</example>

<example>
Good: check account balance  
Bad: perform check  
Explanation: This theme label doesn't specify what category of things needs to be checked (does it relate to an account? the status of something?).  
</example>

<example>
Good: reset password  
Bad: secure account  
Explanation: The theme doesn't describe any particular way of securing an account.  
</example>
</examples>

2C - The theme label is sufficiently general.

Although sets of theme labels may vary according to the desired level of granularity, they should be general enough to classify a range of customer intents. A theme label should rarely classify a singleton intent set, unless an intent is an isolate (has no closely related intents in the dataset).

<examples>
<example>
Good: track order  
Bad: track spoon/fork order  
Explanation: This is too specific since it includes irrelevant information (a description of the items within the order to be tracked).  
</example>

<example>
Good: add individual to policy  
Bad: add oldest child to policy  
Explanation: This is too specific since it includes details that are not needed to identify the resolution steps. The information introduced by *oldest child* would likely be captured later as a part of the resolution steps anyway. It is not needed to understand the basic issue category.  
</example>

<example>
Good: reset password  
Bad: reset password again  
Explanation: This is too specific since it implicitly refers to the existence of a previous reset-password event, which is probably irrelevant for performing a new password reset.  
</example>
</examples>

2D - The theme label lacks context-sensitive meaning.

Natural language contains many expressions that gain meaning from context. For our purposes, the primary concern is to avoid pronouns (him, her, them, it, us, etc.) and demonstratives (this, that, those, etc.), but all other context-sensitive expressions should also be avoided (see examples).

Theme labels that violate 2D will usually (but not necessarily) also violate 2C.

<examples>
<example>
Good: track order  
Bad: track their order  
Explanation: *Their* (a possessive pronoun) is context-sensitive because it refers to whoever the owner of the order is. Also violates 2C.  
</example>

<example>
Good: dispute charge  
Bad: dispute charge from yesterday  
Explanation: *Yesterday* is context-sensitive because it refers to whatever day is before the day of contact. Also violates 2C.  
</example>

<example>
Good: close account  
Bad: close that account  
Explanation: *That* is a demonstrative; it depends on the context of a conversation to know precisely what is being talked about. Also violates 2C.  
</example>

<example>
Good: find nearest branch  
Bad: find nearest one  
Explanation: Expressions like *one* depend on context in order to understand (A: "Sorry, what did you say about branches?" B: "Find the nearest one.").  
Bad: find closest  
Explanation: This is not acceptable either since it requires context to understand what needs to be found (nearest branch in the area? nearest available appointment?).  
</example>
</examples>'''
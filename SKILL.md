---
name: technical-english
description: Write, rewrite or check text in Technical English, a controlled English in which every sentence has one parse and every term one meaning. Use this whenever the user asks for technical English or controlled English, and for software documentation that must be unambiguous, easy to translate or easy for non-native readers - READMEs, install and setup guides, runbooks, API and CLI reference, error messages, UI text, release notes, code comments - as well as general text (emails, policies, announcements) that must have only one possible reading. Trigger even if the user only pastes a few sentences and says "make this technical English", "make this unambiguous", "make this translation-ready" or "check this for ambiguity".
---

# Technical English

Technical English is a controlled subset of English. Its rules come from published research on controlled languages for machine translation (the KANT system at Carnegie Mellon). In that work, writers used a checker that rejected any sentence it could not parse to exactly one meaning, and the text was then machine-translated into several languages.

This skill applies those rules to any technical or general text. The main use is software documentation. The goal is: **each sentence must have one parse and each term one meaning, so that a translation engine, a non-native reader or a reader in a hurry cannot misread it.** When no rule covers a case, choose the wording that leaves the fewest possible readings.

This skill is not ASD-STE100 Simplified Technical English. STE restricts writers to about 900 approved general words and sets word-count limits. Technical English allows a large technical vocabulary but gives each term exactly one meaning, and it controls grammar tightly. Do not import STE's word list or word limits as rules of this skill.

## Sources and limits

The grammar rules come from the published research (sources are in `references/rules.md`); apply them with confidence. There is no fixed word list, so apply the vocabulary *principles*: one meaning per term, one term per concept, no invented noun stacks. A glossary or style guide from the user overrides your own term choices.

## Reference files

- `references/rules.md` - the full rule set, with the reason for each rule and before/after examples. Read it the first time you use the skill in a conversation, and whenever a sentence does not fit the core rules below.
- `references/software.md` - read for any software text: what you must never rewrite (code, identifiers, UI labels), terminology with two meanings in software, procedures, reference docs, error messages, RFC 2119 keywords.
- `scripts/check_text.py` - a pattern checker (see step 5).

## Workflow

1. **Identify the text type**, because the structure rules depend on it: procedure, reference, conceptual description, troubleshooting, UI/error text, or general correspondence.
2. **Protect what must not change.** Code, commands, identifiers, file paths, config keys, API names, UI labels, error strings, URLs and version numbers stay exactly as they are. Only the prose around them follows the rules.
3. **Resolve every ambiguity before you rewrite.** If a source sentence has two possible meanings (a modifier that can attach two ways, "it" with two candidate antecedents, "and" with unclear scope, "since" as time or cause), choose the reading that the context supports and record the choice. Do not resolve silently.
4. **Fix terminology, then rewrite sentence by sentence** with the core rules below. Use one term per concept for the whole text.
5. **Run the checker**: `python scripts/check_text.py <file>` (or pipe text on stdin). It skips fenced code, inline code, URLs, headings and tables. It reports patterns only, so read each flag and decide. It cannot find wrong terms, unclear antecedents or attachment problems; step 3 covers those.
6. **Deliver** the rewritten text, then a short list of the disambiguation choices and any terms the user should confirm. Keep the notes short; the user wants the text.

If the user asks you only to *check* text, report each violation with the rule number, the words, and a compliant rewrite.

## Core rules

**Vocabulary**
- One meaning per word per part of speech. If a word has two senses in the text, use a different word for one of them, and keep that split everywhere ("problem", not "issue", when you also refer to GitHub issues).
- One term per concept. Do not vary words for style ("directory" everywhere, not "directory" and "folder").
- Prefer a single-word verb to a verb + particle: "start", not "spin up"; "delete", not "clean up"; "enable", not "turn on"; "configure", not "set up". A phrasal verb that is the product's own UI term ("Sign in") stays.
- No invented noun stacks. Use a compound only when it is an established term ("access token", "load balancer"). Otherwise use "of", "for" or a relative clause.
- Give fixed meanings to modal verbs: "must" = requirement, "can" = ability or permission, "do not" = prohibition. Avoid lowercase "should", "might", "could" and "would" in instructions. Specifications that adopt RFC 2119 keep their uppercase MUST/SHOULD/MAY.
- Avoid connectives with two meanings: use "because" for cause and "after"/"since [time]" for time; do not use "as" or "once" to start a clause; use "while" only for time.
- No contractions, no "and/or", no idioms, no Latin abbreviations ("e.g.", "i.e.", "etc.").

**Phrases**
- Use a determiner with nouns in full sentences: "Run the command.", not "Run command." Give identifiers a category noun: "the `timeout` parameter", "the `users` table".
- Do not coordinate verbs that share an object: "Stop and remove the container" becomes "Stop the container. Remove the container."
- Repeat the preposition when scope could be unclear: "in the config file and in the environment", not "in the config file and environment".
- A quantifier needs a noun: "until no jobs remain", not "until none remain".

**Sentences**
- A subordinate clause needs its own subject and finite verb: "When deploying," becomes "When you deploy,". "If not found," becomes "If the server does not find the record,". The test: delete the conjunction; the clause must stand alone as a sentence.
- Do not start a sentence with a participle phrase: "Using the CLI, you can..." becomes "You can use the CLI to...".
- No reduced relatives: "the value returned by the API" becomes "the value that is returned by the API" or "the return value of the API". (Not "the value that the API returns", which is an object relative; see the next rule.)
- Introduce relative clauses with "that" or "which", and keep the relative pronoun as the subject of its clause ("the service that handles requests"). Restructure object relatives ("the file you created") and prepositional relatives ("the server to which you connect").
- Join clauses with "and" or "but" only when both are the same type (two commands, or two statements).
- No ellipsis, except a small fixed set ("if necessary", "if applicable").
- Avoid WH-questions in headings and troubleshooting; use statements or yes/no questions.
- Limit pronouns. Use "it" or "they" only when the antecedent is unmistakable within the same sentence. Never start a sentence with "This", "That" or "It" for a whole previous idea; name the idea ("This change...", "This error...").
- If a prepositional phrase could attach to the verb or to the noun, restructure: "Configure the client with TLS" becomes "Use TLS to configure the client" or "Configure the client that uses TLS".
- One instruction or one fact per sentence. There is no fixed word limit; long sentences produce scope and attachment ambiguity, so split them.

**Structure**
- Procedures are numbered steps in imperative mood, one action per step. Put a condition before the action ("If you use Windows, ..."). Put the expected result in a separate sentence.
- Warnings state the hazard, the consequence and the action to avoid it, as separate sentences, under a marked label (Warning, Caution, Note).
- Keep document structure explicit: headings, numbered lists, tables and admonitions, not run-in prose.
- Write numbers, units, dates, times, versions and identifiers in one fixed format. Add a time zone to times. Write dates unambiguously ("15 October 2026" or "2026-10-15", not "10/15/26").

## General (non-technical) text

The vocabulary and sentence rules apply unchanged. Adjust only the structure:
- Greetings, sign-offs, headings and table cells can be short phrases.
- Put one topic in each paragraph. State a request or decision directly in its own sentence ("Please send the report by 20 October 2026."), not as a hint.
- Remove idioms, metaphors, humor that depends on wording, and cultural references. They have no single literal meaning and do not translate.
- Technical English reads plain and repetitive by design. Do not add variety back in. If the user wants a warmer tone, use polite fixed phrases ("Thank you for...") rather than idiom.

## Example (software)

Source:
> To get started, spin up the dev server and hit the /health endpoint - if it's not returning 200, check the logs, which you'll find in ./logs, and make sure the DB is up and running.

Technical English:
> 1. Start the development server.
> 2. Send a GET request to the `/health` endpoint.
> 3. Make sure that the response has the status code 200.
>
> If the status code is not 200, do the steps that follow:
> 1. Read the log files in the `./logs` directory.
> 2. Make sure that the database is running.

Notes: "it" read as "the endpoint response". "Dev server" expanded to "development server". The source does not give the start command; add it in a code block after step 1. "Up and running" read as "running". Do not invent commands, flags or paths that the source does not contain.

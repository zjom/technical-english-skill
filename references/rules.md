# Technical English rule reference

Rules are grouped as the published controlled-English research groups them: vocabulary, phrase level, sentence level, document structure, markup and punctuation. Each rule says why it exists, because the reason tells you how to handle cases the rule does not name.

- **[documented]**: the rule comes directly from the published controlled-English research (KANT).
- **[practice]**: standard controlled-language practice that is consistent with the goal of one meaning per sentence but not stated in the published sources. Apply it unless the user's style guide says otherwise.

The rules apply to any technical text. Examples include machinery, software and general text. For software-specific guidance (protected strings, terminology, procedures, reference docs), see `software.md`.

## Contents
1. Vocabulary
2. Phrase-level rules
3. Sentence-level rules
4. Document types and structure
5. Markup, identifiers and punctuation
6. Sources

---

## 1. Vocabulary

**1.1 One meaning per word/part-of-speech pair [documented].** A word used as a verb has one meaning in the text; the same word used as a noun has one meaning. If a word has two senses, express one of them with a synonym and keep that split everywhere.
- Machines: "rip" = break pavement with a ripper; fabric damage = "tear".
- Software: "issue" = a tracker issue; a fault = "problem". "check" = verify; the UI control = "check box".
- General: "address" = a location; the action = "respond to" or "discuss".

**1.2 One term per concept [documented as consistent terminology].** Do not use synonyms for variety. A reader, and a translation engine, assumes that two different words refer to two different things.
- Bad: "Open the folder. Copy the file into the directory."
- Good: "Open the directory. Copy the file into the directory."

**1.3 A large vocabulary, not a small one [documented].** Technical English does not cap the vocabulary. Controlled languages with a very small word list force writers to produce long, convoluted sentences to say complex things. Keep the precise technical term instead. Use the correct term ("hydraulic accumulator", "idempotency key", "garbage collector") rather than a paraphrase. Approved multi-word terms ("oil pan", "access token") are single units: do not insert words into them or reorder them.

**1.4 Phrasal verbs: prefer a single-word verb [documented].** Particles look like prepositions and create parse ambiguity ("look up the table" — find the table, or look up toward it?).

| Avoid | Use |
|---|---|
| turn on / turn off | start / stop (engine), enable / disable (feature) |
| take off / take out / pull out | remove |
| put in / put on | install, insert |
| set up | configure, install, prepare |
| fill up / top up | fill, add |
| fill in / fill out | complete, enter |
| check out | inspect, check (but `git checkout` is a protected command) |
| hook up / plug in | connect |
| let out / bleed off | release |
| find out / figure out | determine |
| look up | find |
| clean up | clean, delete, remove |
| shut down | stop |
| spin up / boot up / bring up | start, create |
| roll back | revert, restore |
| come up / pop up | appear |
| run into | encounter |
| carry out | do, perform |
| follow up | contact again, check again |

If no single verb exists, or the phrasal verb is a fixed product or domain term ("Sign in", "account for"), keep it and use it consistently.

**1.5 Functional words [documented].** Limit pronouns and conjunctions, because each one adds possible parses. Use determiners consistently. Specify quantifiers precisely.

**1.6 Modal verbs [documented that senses must be fixed; the mapping is practice].**
- "must" = requirement. "must not" or "do not" = prohibition.
- "can" = ability, possibility or permission. "cannot" = inability.
- Avoid "should", "might", "could" and "would" in instructions. They blur requirement and recommendation and translate inconsistently. For a recommendation, write "We recommend that you..." or "This step is optional."
- Avoid "may not" (not permitted, or possibly not?).
- Exception: specifications that adopt RFC 2119 keep uppercase MUST/SHOULD/MAY with their defined meanings (see `software.md` §4).

**1.7 Participial forms restricted [documented].** -ing and -ed forms must not head reduced clauses (3.2, 3.4, 3.11). An -ing or -ed form that is part of an approved term ("cooling system", "logging level", "managed identity") is fine.

**1.8 Orthography [documented].** One spelling, one capitalization, one hyphenation and one use of "/" per term ("O-ring" or "o-ring"; "email" or "e-mail"). Keep noun and verb forms apart ("setup" noun / "set up" verb; "backup" / "back up"). Do not use "and/or"; write "A, B, or both" [practice]. Do not use contractions ("it's", "don't", "you'll") [practice].

**1.9 Connectives with two meanings [practice; applies 1.1 to function words].**

| Word | Problem | Write |
|---|---|---|
| since | time or cause | "after" or "since [a time]" for time; "because" for cause |
| as | cause, time, manner or comparison | "because", "when"/"while", "in the same way as" |
| once | "one time" or "after" | "after", "one time" |
| while | time or contrast | "while" for time only; "but" or "however" for contrast |
| when | time or condition | "when" for an event that will occur; "if" for a condition that might not occur |
| then | sequence or consequence | "then" for sequence; for a consequence, write a full "If ..., ..." sentence |
| only | scope depends on position | put "only" directly before the word it limits |

**1.10 Idioms, figures of speech and abbreviations [practice].** An idiom has a figurative meaning that a translation engine renders literally. Remove idioms, metaphors, sports and cultural references, and wordplay.
- "up and running" -> "running"; "out of the box" -> "by default"; "under the hood" -> "internally"; "on the fly" -> "during operation"; "a good rule of thumb" -> "we recommend"; "touch base" -> "talk".
- Replace Latin abbreviations: "e.g." -> "for example"; "i.e." -> "that is"; "etc." -> name all items, or write "and other [category]"; "vs." -> "and" or "compared to"; "via" -> "through" or "by".
- Spell out an abbreviation at first use unless the reader's glossary treats it as a standard term ("API", "URL").

## 2. Phrase-level rules

**2.1 Use determiners [documented].** In full sentences, give nouns a determiner. Determiners tell the translation engine whether a noun is definite, indefinite or plural, which many target languages mark obligatorily.
- Bad: "Install washer on bolt." / "Run command in terminal."
- Good: "Install the washer on the bolt." / "Run the command in a terminal."
Titles, table cells, labels and button text may omit determiners.

**2.2 No verb coordination with a shared object or modifier [documented].**
- Bad: "Extend and retract the cylinders three times." / "Stop and remove the container." / "Review and approve the request by Friday."
- Good: "Extend the cylinders and retract the cylinders. Do this procedure three times." / "Stop the container. Remove the container." / "Review the request. Approve the request by Friday."
Reason: the object and the modifier ("three times", "by Friday") can attach to one verb or to both.

**2.3 Repeat the preposition in coordinated phrases [documented].**
- Ambiguous: "5 cubic meters of concrete and sand" (5 m³ total, or each?)
- Clear: "5 cubic meters of concrete and 5 cubic meters of sand".
- Ambiguous: "Set the variable in the config file and environment."
- Clear: "Set the variable in the config file and in the environment." — or, if only one is meant, say which.

**2.4 Noun compounds only when licensed [documented].** Accept a noun-noun compound only if it is an established term (a part name, a product term, a standard technical term). Break up invented stacks with "of", "for" or a relative clause.
- Bad: "engine oil pressure sensor harness connector clip"
- Bad: "user session token refresh failure handler"
- Good: "the function that handles a failure when the session token of a user is refreshed" — or name it by its identifier: "the `onTokenRefreshError` handler".

**2.5 Quantifiers and partitives need a head noun [documented].**
- Bad: "Repeat these steps until none are left." / "Replace any that are worn." / "Delete some."
- Good: "Repeat these steps until no bolts remain." / "Replace any seals that are worn." / "Delete some of the old logs."

**2.6 Avoid gapped coordination [documented as a known checker problem].** "top and bottom gaps" can parse as "top" + "bottom gaps"; "read and write permissions" can parse as "read" + "write permissions". Write "the top gap and the bottom gap", "the read permission and the write permission".

## 3. Sentence-level rules

**3.1 Coordinated clauses must match in type [documented].** Join two commands or two statements, not one of each.
- Bad: "Remove the filter and the housing will drain." / "Restart the service and the change takes effect."
- Good: "Remove the filter. The housing will drain." / "Restart the service. The change takes effect after the restart."

**3.2 Subordinate clauses need an explicit subject and finite verb [documented].** If you delete the subordinating conjunction, the clause must be a complete sentence.
- "When starting the engine," -> "When you start the engine,"
- "After installing the package," -> "After you install the package,"
- "Before merging," -> "Before you merge the branch,"
- "If damaged, replace the hose." -> "If the hose is damaged, replace the hose."
- "If not found, the function returns null." -> "If the function does not find the record, the function returns `null`."
Exception: a small closed set of fixed elliptical phrases, such as "if necessary", "if equipped" [documented examples], "if applicable" [practice].

**3.3 No ellipsis [documented].** Do not omit words that the reader must reconstruct.
- Bad: "Tighten the front bolts to 50 N·m and the rear to 70 N·m."
- Good: "Tighten the front bolts to 50 N·m. Tighten the rear bolts to 70 N·m."
- Bad: "Use port 80 for HTTP, 443 for HTTPS."
- Good: "Use port 80 for HTTP. Use port 443 for HTTPS."

**3.4 Relative clauses: explicit "that"/"which", subject relatives only [documented].**
- Reduced relative (bad): "the pumps mounted to the pump drive", "the value returned by the API" -> "the pumps that are mounted to the pump drive", "the value that is returned by the API".
- Object relative (bad): "the bolt you removed", "the file that you created" -> restructure: "Install the bolt. You removed this bolt in Step 3." or name it: "the mounting bolt", "the `config.yml` file".
- Complex relative (bad): "the server to which you connect" -> "the server that accepts your connection" or "Connect to the server. The server..."
- Subject relative (good): "the valve that controls the flow", "the service that handles the requests".
[practice] Use "that" for restrictive clauses. Do not use a "which" clause to add a separate statement; write a separate sentence.

**3.5 Avoid WH-questions [documented].** Use statements or yes/no questions.
- "What is the oil pressure?" -> "Check the oil pressure."
- "Why does the build fail?" (heading) -> "The build fails" or "Causes of build failures".
- In general text, ask the question as a direct request: "What time suits you?" -> "Please tell me a time that is convenient for you."

**3.6 Pronouns [documented as "limit"].** Use "it", "they", "this" and "these" only when the antecedent is unmistakable and close, ideally in the same sentence with only one possible candidate. Otherwise repeat the noun. Do not start a sentence with "This", "That" or "It" to refer to a whole previous idea; name the idea ("This change", "This error").
- Bad: "Disconnect the hose from the valve and cap it." (hose or valve?)
- Good: "Disconnect the hose from the valve. Install a cap on the hose."
- Bad: "The client sends the token to the server. It validates it."
- Good: "The client sends the token to the server. The server validates the token."

**3.7 Prepositional-phrase attachment [documented: authors disambiguated these interactively].** If a phrase with "with", "by", "for", "on", "in" or "at" can modify the verb or the noun before it, restructure.
- "Secure the gear with twelve rivets." -> "Use twelve rivets to secure the gear."
- "Configure the client with TLS." -> "Use TLS to configure the client." or "Configure the client that uses TLS."
- "Email the report to the team on Friday." -> "On Friday, email the report to the team."

**3.8 Adverb attachment [documented as a checker problem].** An adverb directly before a preposition can attach to the verb.
- "Do not stand directly under a hoist." -> "Do not stand in the area directly below a hoist."
- "Deploy only to staging." -> put "only" before the word it limits, and check the meaning: "Deploy to the staging environment only."

**3.9 Short, single-purpose sentences [practice].** There is no fixed word limit, but long sentences multiply attachment and scope ambiguity. Aim for one instruction or one fact per sentence. The checker flags sentences over 25 words for review.

**3.10 Voice [practice].** Use the active voice with an explicit actor ("Remove the bolt.", "The scheduler starts the job."). The passive is acceptable in descriptions when the actor is unknown or irrelevant ("The valve is installed in the head."), and in subject relatives ("the files that are stored in the bucket"). Do not use a passive that hides which component acts.

**3.11 No opening participle phrases [practice; extends 3.2].** A sentence that starts with an -ing or -ed phrase has no explicit subject for that phrase.
- "Using the CLI, you can deploy the app." -> "You can use the CLI to deploy the app."
- "Built on Postgres, the service stores..." -> "The service is built on Postgres. The service stores..."
- "Having reviewed the proposal, we agree." -> "We reviewed the proposal. We agree with the proposal."
"During" and other prepositions are not participles and are fine.

## 4. Document types and structure [practice, consistent with documented markup rules]

**4.1 Procedures.** Numbered steps in imperative mood, one action per step, in the order of performance. Put a condition before the action ("If the pressure is above 200 kPa, release the pressure."). Put the result or the check in a separate step or sentence.

**4.2 Warnings and cautions.** State the hazard, the consequence and the avoidance as separate, complete sentences. Keep the signal word (WARNING, CAUTION, NOTE, or the platform's admonition labels) as a marked element, not inside a sentence.
> WARNING
> Hot oil can cause burns. Let the engine cool before you remove the drain plug.

> Warning
> This command deletes all data in the database. You cannot recover the data. Create a backup before you run the command.

**4.3 Notes.** A note gives information, not a step. Do not hide an instruction in a note.

**4.4 Descriptions.** Present-tense declaratives. One function per sentence. "The pump pulls fuel from the tank. The pump sends the fuel to the filter." / "The gateway receives each request. The gateway sends the request to a worker."

**4.5 Titles and labels.** Titles, table cells, labels and buttons may be noun phrases or imperative fragments and may omit determiners. Use one pattern throughout a document set.

**4.6 Correspondence and general text.** Greetings and sign-offs may be fragments. One topic per paragraph. State requests and decisions directly, each in its own sentence, with a date if there is a deadline. Use polite fixed phrases instead of idioms.

## 5. Markup, identifiers and punctuation

**5.1 Mark document structure [documented].** In the published systems, text was authored in SGML with tags for titles, paragraphs, lists, tables, warnings, callouts and measurements. In Markdown, HTML or plain text, keep the same structure visible: headings, numbered lists, labelled admonitions, tables, code blocks. Do not run list items into a sentence.

**5.2 Callouts vs quantities [documented].** Numbers that refer to illustration callouts, line numbers or step numbers must not be confusable with quantities. Use one labelled convention ("the bolts (Callout 3)", "line 42", "Step 3") and write quantities as numbers with a noun ("two bolts", "3 retries").

**5.3 Measurements and values [documented].** Keep a fixed pattern for units, dual units and tolerances ("42.931 ± 0.013 mm (1.6902 ± 0.0005 inch)", "30 seconds", "512 MB"). Do not change the order or the format within a document.

**5.4 Special forms [documented].** Part numbers, serial numbers, model names, dates, version numbers, identifiers, code and UI labels follow one fixed format and are never reworded. Give each one a category noun in the sentence ("the part 1R-0750", "the `timeout` parameter").

**5.5 Punctuation [documented that rules must be fixed; specific uses are practice].**
- Comma: after an introductory subordinate clause; the serial comma in lists.
- Colon: only to introduce a list, a code block or a value.
- Semicolon: avoid; use two sentences.
- Parentheses: for callouts, units, abbreviations at first use, identifiers and part numbers. Not for asides or hidden steps.
- Quotation marks: only for exact text that appears on screen or on the machine, or use one consistent style (bold for UI labels, code format for identifiers).
- Dashes: do not use a dash to join two clauses; write two sentences.

## 6. Sources

- Mitamura, T. and Nyberg, E. (1995). "Controlled English for Knowledge-Based MT: Experience with the KANT System." Proceedings of TMI-95, Leuven. https://aclanthology.org/1995.tmi-1.12/ — primary source for the documented rules.
- Nyberg, E. and Mitamura, T. (1996). "Controlled Language and Knowledge-Based Machine Translation: Principles and Practice." Proceedings of CLAW-96.

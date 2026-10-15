# Technical English for software documentation

This file applies the rules in `rules.md` to software text. Rule numbers in brackets point to `rules.md`.

## Contents
1. What you never rewrite
2. Naming identifiers in prose
3. Terminology
4. Modal verbs and RFC 2119
5. Procedures (install, setup, how-to, runbooks)
6. Reference documentation (API, CLI, config)
7. Conceptual and architecture text
8. Troubleshooting
9. Error messages and UI text
10. Release notes and changelogs
11. Code comments and commit messages
12. Numbers, units, dates and versions

---

## 1. What you never rewrite

These items are the software equivalent of tagged part numbers and callouts [5.4]: fixed strings that the translation engine and the reader must take exactly as written. Keep them byte-for-byte, even when they break a rule in this skill.

- Code blocks, inline code, shell commands, flags and their values (`git checkout`, `--dry-run`, `set -e`)
- Identifiers: function, class, variable, parameter, field, table, endpoint, event and package names (`setUp`, `onLoad`, `turnOff()`)
- File names and paths, environment variables, config keys
- UI labels: button, menu, tab, field and dialog names. Copy the exact label and format it consistently, for example in bold: Select **Sign in**.
- Error message text and log output that the reader will see on screen. Quote it exactly in a code block or in quotation marks.
- URLs, version numbers, product and trademark names

A phrasal verb or contraction inside a protected string is not a violation. The prose around the string still follows the rules.

## 2. Naming identifiers in prose

**2.1 Give each identifier a category noun [2.1, 5.4].** The noun tells the reader (and a translation engine, which cannot parse `maxRetries`) what kind of thing the identifier is. It also gives the sentence a normal noun phrase, with a determiner.
- Bad: "Set `maxRetries` to 5."
- Good: "Set the `maxRetries` parameter to 5."
- Bad: "`users` stores account data."
- Good: "The `users` table stores the account data."

**2.2 Do not inflect or verb an identifier.** Do not add endings to code, and do not use a command name as a verb.
- Bad: "the `Item`s", "after you `git push`ed", "`curl` the endpoint"
- Good: "the `Item` objects", "after you run the `git push` command", "use the `curl` command to send a request to the endpoint"

**2.3 Do not use an identifier as the only name of a concept.** At first use, say what it is: "The `ttl` field sets the time to live (the time that a record stays in the cache)."

## 3. Terminology

**3.1 One term per concept [1.1].** Choose one term from each pair and use it in the whole document set. Put the choices in a glossary if the user does not already have one.

| Pick one | Notes |
|---|---|
| directory / folder | "directory" for CLI and code; "folder" only if the product UI says "folder" |
| sign in / log in | follow the product UI |
| select / click / tap / choose | "select" works for mouse, touch and keyboard |
| enter / type | "enter" |
| parameter / argument | "parameter" in a definition, "argument" for the value passed in a call; keep the distinction strict or use only "parameter" |
| error / exception | "exception" only for the language construct |
| repository / repo | "repository" |
| app / application | one |
| configuration / settings / options / preferences | follow the UI; do not mix |
| delete / remove | "delete" = data is gone; "remove" = item is taken out of a list or group but still exists |
| start / launch / run / execute | "start" for services and apps, "run" for commands and scripts |

**3.2 Words with two meanings in software [1.1].** Split each sense with a different word and keep the split.

| Word | Sense to keep | Other sense: write |
|---|---|---|
| issue | GitHub/Jira issue | "problem" |
| check | verify | "select the check box" for the UI control |
| flag | command-line option ("the `--force` flag") | "mark" for the action |
| return | a function returns a value | "go back" for navigation |
| run | to execute a command | "a run" (noun) -> "an execution" or "a job", if both senses appear |
| release | a published version | "free" (memory), "unlock" (a lock) |
| commit | a Git commit | "save" or "apply" for other changes |
| instance | an object of a class *or* a virtual machine | choose one; write "VM instance" or "object" for the other |
| hit | (avoid) | "send a request to" (endpoint), "reach" (a limit), "match" (cache hit is an approved term) |
| fire | (avoid) | "trigger" or "emit" (an event) |
| kill | (avoid unless it is the `kill` command) | "stop" or "end" (a process) |
| drop | a database table or connection: avoid | "delete" (table), "close" (connection), "discard" (packets) |
| hang | (avoid) | "stop responding" |
| spin up | (avoid) | "start", "create" |
| client | the software that sends requests | "customer" for a person or organization |
| service | a software service | "support" for customer help |

**3.3 Phrasal verbs in software [1.4].**

| Avoid | Use |
|---|---|
| set up (verb) | configure, install, create |
| turn on / turn off (a feature) | enable / disable |
| spin up / boot up / bring up | start, create |
| shut down (a service) | stop |
| tear down | delete, remove |
| clean up | delete, remove |
| roll back | revert, restore (a deployment) |
| look up | find |
| find out / figure out | determine |
| fill in / fill out | complete, enter |
| pop up / come up | appear |
| kick off | start |
| run into | encounter, get |
| hook up / plug in | connect |
| carry out | do, perform |
| back up (verb) | Keep if it is the product term; otherwise "create a backup of" |
| log in / sign in | Keep the product's UI term; as a noun write "sign-in" consistently |

Orthography [1.8]: keep noun and verb forms apart: "setup" (noun) vs "configure" (verb); "login" (noun, if the product uses it) vs "sign in" (verb); "backup" (noun) vs "back up" (verb).

**3.4 Noun stacks [2.4].** Software text produces long stacks. Keep a stack only if it is an established term in the product ("access token", "connection pool", "rate limit"). Break up the rest.
- Bad: "the database connection pool timeout retry setting"
- Good: "the setting that controls retries after a timeout in the database connection pool" — or, better, name it by its key: "the `pool.retryOnTimeout` setting".

## 4. Modal verbs and RFC 2119

**4.1 Normal documentation [1.6].** "must" = requirement, "must not" / "do not" = prohibition, "can" = ability or permission. Avoid lowercase "should", "may", "might", "could" and "would". If something is recommended but optional, say so: "We recommend that you enable TLS." or "This step is optional."

**4.2 Specifications that adopt RFC 2119 / RFC 8174.** If the document declares these keywords, keep MUST, MUST NOT, SHOULD, SHOULD NOT and MAY in uppercase with their defined meanings, and do not use the lowercase forms of these words for any other meaning. The checker ignores uppercase keywords.

## 5. Procedures (install, setup, how-to, runbooks)

Structure:
1. Title: a task name, in one fixed pattern for the whole set ("Install the CLI" or "Installing the CLI" — not both).
2. Prerequisites: a list, each item a full sentence or a fixed noun phrase.
3. Steps: numbered, imperative, one action per step [4.1].
4. Result: one sentence that says what the reader sees when the procedure is complete.

Rules:
- Put the command in a code block *after* the step sentence. The step sentence names the action: "Install the dependencies." then the code block.
- Put a condition before the action: "If you use Windows, run the command that follows in PowerShell."
- Platform variants: separate, labelled sub-lists or tabs, not "on Mac, do X; on Linux, Y" in one sentence [3.3 ellipsis].
- Put the expected output in a separate sentence: "The terminal shows the version number."
- Placeholders: one fixed format (`<project-id>`, in angle brackets), and say what to replace: "Replace `<project-id>` with the ID of your project."
- Do not hide a step in a note or in a parenthesis.
- "Optional" steps start with "Optional:".

Before:
> Clone the repo and cd into it, then install deps (if you haven't already) and copy .env.example to .env, filling in your API key.

After:
> 1. Clone the repository.
>    ```
>    git clone https://example.com/org/app.git
>    ```
> 2. Go to the directory of the repository.
>    ```
>    cd app
>    ```
> 3. If the dependencies are not installed, install the dependencies.
>    ```
>    npm install
>    ```
> 4. Copy the `.env.example` file to a new file with the name `.env`.
> 5. In the `.env` file, set the `API_KEY` variable to your API key.

(The repository URL and the `API_KEY` name are examples. Use only commands and names that the source or the user gives.)

## 6. Reference documentation (API, CLI, config)

- Description fields in tables can use one fixed fragment pattern, as the rules allow for titles and labels [4.5]. Choose one pattern and keep it:
  - Parameters and fields: a noun phrase with a determiner: "The maximum number of retries."
  - Functions and endpoints: either "Returns the ID of the user." in every entry, or a full sentence "The function returns the ID of the user." in every entry. Do not mix.
- Prose paragraphs in reference pages use full sentences.
- State defaults, types, units and limits in separate, fixed columns or sentences: "The default value is 30. The unit is seconds."
- State behavior in each case as a full conditional sentence, not ellipsis:
  - Bad: "Returns null if not found."
  - Good: "If the record does not exist, the function returns `null`."
- Side effects and errors: one sentence each. "The function deletes the cache entry. If the key does not exist, the function throws a `KeyError` exception."
- Avoid "it" for the function or endpoint across sentences; repeat "the function", "the endpoint", "the command".

## 7. Conceptual and architecture text

- Present-tense declaratives, one function per sentence [4.4]: "The gateway receives each request. The gateway sends the request to a worker."
- Name actors explicitly. In "The request is validated and then queued", the reader cannot tell which component does each action. Write "The gateway validates the request. The gateway puts the request in the queue."
- Do not use metaphor as explanation ("the scheduler is the brain of the system"). State the function.
- "you" = the reader. "the user" = the end user of the reader's software. Define this once if both appear.

## 8. Troubleshooting

- Use a statement or yes/no question as the heading, not a WH-question [3.5]: "The server does not start" or "Error: connection refused".
- Structure each entry as Problem, Cause, Solution. Each is one or more full sentences.
- Quote the error text exactly in a code block.

## 9. Error messages and UI text

- Two parts, two sentences: what happened, then what the reader can do. "The file is larger than 10 MB. Select a file that is 10 MB or smaller."
- No pronouns without a clear antecedent ("It failed"), no idioms ("Oops", "Something went sideways"), no blame ("You entered an invalid date" -> "The date is not valid. Enter the date in the format YYYY-MM-DD.").
- Button labels: a verb + noun in one pattern ("Save changes", "Delete project"). Labels are titles, so they can omit determiners.
- Keep the same term in the UI, the error messages and the documentation.

## 10. Release notes and changelogs

- One change per entry. Entries can use a fixed pattern ("Added", "Fixed", "Changed", "Removed" as category headings), then a full sentence: "The `export` command now supports the CSV format."
- For a fix, state the old behavior and the new behavior: "Previously, the client did not retry a request after a timeout. Now, the client retries the request three times."
- Breaking changes go under a marked label, with the action the reader must take as an imperative sentence.

## 11. Code comments and commit messages

- Apply the rules to the prose only. Code, identifiers and conventional prefixes ("feat:", "fix:") stay.
- A commit subject line can be a fixed imperative fragment ("Add retry to the upload client"). The body uses full sentences.
- Comments state why, in full sentences, with explicit subjects. "Retry because the API returns 503 under load." -> "The client retries the request because the API returns status 503 when the load is high."

## 12. Numbers, units, dates and versions [5.3]

- Dates: "15 October 2026" or "2026-10-15". Never "10/15/26" or "15/10/26".
- Times: 24-hour or with AM/PM, always with a time zone: "14:00 UTC".
- Durations and sizes in prose: number + unit word or standard symbol with a space: "30 seconds", "512 MB". Decide whether MB means 10⁶ or 2²⁰ bytes, and keep it (or use MiB).
- Versions: "version 2.3.0 and later", not "2.3+". Ranges: "from 1 to 10 (inclusive)".
- Numbers: one style for the document (digits for all technical values).

# Technical English Skill

This repository contains an agent skill that writes, rewrites and checks text in Technical English. Technical English is a controlled subset of English. In Technical English, each sentence has one parse and each term has one meaning. The rules come from research on the KANT controlled language at Carnegie Mellon University.

The main use is software documentation, for example READMEs, guides, API reference, error messages and release notes. The skill also applies to general text, for example emails and policies.

Technical English is not ASD-STE100 Simplified Technical English. The skill does not use a fixed word list or a word limit.

## Contents

| Path | Content |
|------|---------|
| `SKILL.md` | The workflow and the core rules |
| `references/rules.md` | The full rule set, with reasons and examples |
| `references/software.md` | Rules for software text |
| `scripts/check_text.py` | A pattern checker |

## Installation

Copy this directory into the skills directory of your agent. For Claude Code, the skills directory is `~/.claude/skills/`.

## Usage

Ask the agent to write or check text in Technical English. For example: "Rewrite this README in Technical English."

You can also run the checker without the agent. The checker requires Python 3.

```sh
python scripts/check_text.py file.md
cat file.txt | python scripts/check_text.py
python scripts/check_text.py --json file.md
```

The checker finds patterns only. The checker cannot find wrong terms or unclear pronouns. Read each result before you change the text.

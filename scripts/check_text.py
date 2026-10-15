#!/usr/bin/env python3
"""Heuristic checker for Technical English (controlled English) style.

Flags patterns that the rules in references/rules.md prohibit and that can
be detected with regular expressions. It is a screening aid: expect some false
positives, and expect it to miss semantic problems (wrong term, unclear
antecedent, attachment). Read every flag before you change the text.

The checker understands Markdown and software text. It does not check:
fenced code blocks, inline code, URLs, Markdown headings, table rows, HTML
tags, or uppercase RFC 2119 keywords (MUST, SHOULD, MAY). Inline code is
replaced with the token CODE, so "Run `npm install`." is checked as
"Run CODE.".

Usage:
    python check_text.py file.md
    cat file.txt | python check_text.py
    python check_text.py --json file.md
    python check_text.py --tables file.md      # also check table cells
"""
import json
import re
import sys

SUBORDINATORS = r"(?:when|while|before|after|if|unless|until|since|once|although|because|whenever)"

PHRASAL_VERBS = {
    # general / machinery
    "turn on": "start / enable",
    "turn off": "stop / disable",
    "take off": "remove",
    "take out": "remove",
    "put in": "install / insert",
    "put on": "install",
    "put back": "install again",
    "pull out": "remove",
    "fill up": "fill",
    "top up": "fill / add",
    "fill in": "complete / enter",
    "fill out": "complete",
    "tighten up": "tighten",
    "check out": "inspect / check",
    "hook up": "connect",
    "plug in": "connect",
    "let out": "release",
    "bleed off": "release",
    "find out": "determine",
    "figure out": "determine",
    "set up": "configure / install / prepare",
    "clean up": "clean / delete / remove",
    "back off": "loosen",
    "line up": "align",
    "shut off": "stop / close",
    "shut down": "stop",
    "carry out": "do / perform",
    "follow up": "contact again / check again",
    # software
    "spin up": "start / create",
    "boot up": "start",
    "bring up": "start / open",
    "tear down": "delete / remove",
    "roll back": "revert / restore",
    "look up": "find",
    "pop up": "appear",
    "come up": "appear",
    "kick off": "start",
    "run into": "encounter",
    "hand off": "send / transfer",
    "point at": "refer to / use",
    "sign off": "approve",
    "log out": "sign out (if that is the UI term)",
    "build out": "build / extend",
    "rule out": "exclude",
}

# Informal software verbs that have a second, figurative meaning [software.md 3.2]
SLANG_VERBS = {
    r"\bhit(?:s|ting)?\s+(?:the|an?|this|that|CODE)\b": "hit -> send a request to / reach",
    r"\bfire[sd]?\b|\bfiring\b": "fire -> trigger / emit",
    r"\bkill(?:s|ed|ing)?\s+(?:the|a|an|this|that|all)\b": "kill -> stop / end",
    r"\bhang(?:s|ing)?\b": "hang -> stop responding",
    r"\bnuke[sd]?\b": "nuke -> delete",
    r"\bblow(?:s|n)? away\b": "blow away -> delete",
    r"\bbump(?:s|ed)?\s+(?:the\s+)?(?:version|dependency|dependencies)\b": "bump -> increase / update",
    r"\bcd\s+into\b": "cd into -> go to (the directory)",
    r"\bgrab(?:s|bed)?\b": "grab -> get / download / copy",
    r"\bping(?:s|ed)?\s+(?:me|us|the team|someone)\b": "ping -> contact / send a message to",
}

ALLOWED_ELLIPTICAL = {"if necessary", "if equipped", "if required", "if applicable", "if needed"}

DETERMINERS = {
    "the", "a", "an", "all", "each", "every", "any", "no", "this", "that", "these",
    "those", "your", "my", "our", "its", "their", "another", "other", "both", "some",
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "several", "many", "more", "only", "clean", "new", "fresh", "hot", "cold", "dry",
    "approved", "specified", "following", "same",
}

IMPERATIVE_VERBS = (
    "Remove|Install|Inspect|Check|Clean|Tighten|Loosen|Replace|Connect|Disconnect|"
    "Drain|Fill|Lubricate|Adjust|Measure|Apply|Release|Run|Open|Close|Select|Enter|"
    "Configure|Deploy|Create|Delete|Update|Restart|Add|Set|Copy|Edit|Save|Upload|"
    "Download|Enable|Disable|Call|Pass|Import|Export|Build|Start|Stop|Send|Read|Write|"
    "Review|Approve|Submit|Attach|Verify|Merge|Push|Pull|Clone|Change|Move|Rename|Use"
)

RULES = []


def rule(rule_id, description):
    def deco(fn):
        RULES.append((rule_id, description, fn))
        return fn
    return deco


@rule("3.2", "Subordinate clause without explicit subject (conjunction + -ing)")
def subordinate_ing(s):
    for m in re.finditer(rf"\b{SUBORDINATORS}\s+(\w+ing)\b", s, re.I):
        if m.group(1).lower() in {"nothing", "something", "anything", "everything", "during", "string", "thing"}:
            continue
        yield m.group(0)


@rule("3.2", "Elliptical subordinate clause (conjunction + adjective/participle, no subject)")
def subordinate_elliptical(s):
    pat = (rf"\b({SUBORDINATORS})\s+(?:not\s+)?(\w+(?:ed|en)|necessary|equipped|required|applicable|"
           r"possible|needed|damaged|worn|loose|hot|cold|found|set|empty|missing|present|available|"
           r"enabled|disabled|true|false|null|successful|unsuccessful|done|complete)\b(?=\s*[,.;)])")
    for m in re.finditer(pat, s, re.I):
        if m.group(0).lower() in ALLOWED_ELLIPTICAL:
            continue
        yield m.group(0)


@rule("3.11", "Sentence starts with a participle phrase (no explicit subject)")
def opening_participle(s):
    m = re.match(r"\s*(?:\d+\.\s*)?([A-Z][a-z]+(?:ing|ed))\b[^.,]*,", s)
    if m and m.group(1).lower() not in {"during", "nothing", "something", "everything", "according", "regarding", "following", "notwithstanding"}:
        yield m.group(0).strip()


@rule("3.4", "Possible reduced relative clause (noun + past participle + preposition)")
def reduced_relative(s):
    pat = (r"\b(?:the|a|an|all|each|any|every)\s+(?:[\w-]+\s+){0,2}?([\w-]+?s?)\s+"
           r"([a-z]+ed|[a-z]+en|built|set|sent|kept|held|found|made|run|written|stored|located)\s+"
           r"(to|on|in|into|onto|by|from|with|at|under|between|for|inside|outside|as)\b")
    for m in re.finditer(pat, s):
        noun, part = m.group(1).lower(), m.group(2).lower()
        if noun in {"is", "are", "was", "were", "be", "been", "has", "have", "that", "which", "you", "we", "they", "it", "can", "must", "will", "not"}:
            continue
        if part in {"often", "open", "even", "seven", "ten", "when", "then", "token", "chicken", "hidden", "kitten", "given"}:
            continue
        if re.search(r"\b(?:that|which)\b", m.group(0), re.I):
            continue
        yield m.group(0)


@rule("3.4", "Object or prepositional relative clause")
def object_relative(s):
    for m in re.finditer(r"\b(?:to|with|from|in|on|by|for|of|at)\s+(?:which|whom)\b", s, re.I):
        yield m.group(0)
    for m in re.finditer(r"\b(?:that|which)\s+(?:you|we|they|it|he|she|users?|the (?:user|operator|technician|client|server|team))\s+(?!is\b|are\b|was\b|were\b)\w+", s, re.I):
        yield m.group(0)


@rule("1.4", "Phrasal verb; prefer a single-word verb")
def phrasal(s):
    low = s.lower()
    for pv, repl in PHRASAL_VERBS.items():
        verb, particle = pv.split()
        infl = r"(?:s|es|ed|d|ing|n|ning|ped|ping|ted|ting|ked|king|t)?"
        direct = rf"\b{verb}{infl}\s+{particle}\b"
        split = rf"\b{verb}{infl}\s+(?:the|a|an|this|that|these|those|all|it|them|your)\s+(?:[\w-]+\s+){{0,2}}?{particle}\b"
        if re.search(direct, low) or re.search(split, low):
            yield f"{pv} -> {repl}"


@rule("1.1", "Informal verb with a second meaning")
def slang(s):
    for pat, repl in SLANG_VERBS.items():
        if re.search(pat, s, re.I):
            yield repl


@rule("2.2", "Coordinated verbs sharing an object (e.g. 'Stop and remove the ...')")
def verb_coordination(s):
    m = re.match(r"\s*(?:\d+\.\s*)?([A-Z][a-z]+)\s+(?:and|or)\s+([a-z]+)\s+(?:the|a|an|all|each|any|your|CODE)\b", s)
    if m:
        yield m.group(0).strip()
    for m in re.finditer(r"(?:,|;|\bthen|\byou|\bplease|\bto|\bcan|\bmust|\bwill)\s+(?:then\s+)?([a-z]+)\s+(?:and|or)\s+([a-z]+)\s+(?:the|a|an|all|each|any|your)\b", s):
        if m.group(1) in {"and", "or", "but", "then", "you", "we", "it", "they"}:
            continue
        yield m.group(0).lstrip(",; ")


@rule("2.5", "Quantifier or partitive without a head noun")
def bare_quantifier(s):
    for m in re.finditer(r"\b(none|some|any|all|each|both|several|many|few|most)\s+(?:are|is|remain|remains|of them|left)\b", s, re.I):
        yield m.group(0)
    for m in re.finditer(r"\b(?:any|some|all|none)\s+that\b", s, re.I):
        yield m.group(0)


@rule("3.6", "Pronoun with possibly unclear antecedent")
def pronouns(s):
    # Demonstrative or personal pronoun used as subject at sentence start
    pat = (r"(?:^|[.;:]\s+|\d+\.\s+)(It|They|This|That|These|Those)\s+"
           r"(?:is|are|was|were|will|can|cannot|must|does|do|did|has|have|had|means|allows|causes|"
           r"makes|ensures|lets|happens|requires|returns|fails|works|runs|gives|shows|depends|"
           r"prevents|helps|uses|sends|creates|contains|should|may|might|could|would)\b")
    for m in re.finditer(pat, s):
        yield m.group(1)
    for m in re.finditer(r"\b(?:and|then)\s+\w+\s+(it|them)\b", s, re.I):
        yield m.group(0)
    for m in re.finditer(r"(?:,\s+\w+|\b(?:into|onto|to|from|in|on|with|for))\s+(it|them)\b(?!\s+(?:is|are|was|were))", s):
        if not re.search(r"\b(?:and|then)\s+\w+\s+(?:it|them)\b", s, re.I):
            yield m.group(0).lstrip(", ")


@rule("1.8", "Contraction; write the full form")
def contractions(s):
    for m in re.finditer(r"\b\w+(?:'|’)(?:s|re|ll|ve|d|t|m)\b", s, re.I):
        w = m.group(0).lower().replace("’", "'")
        if w.endswith("'s") and w not in {"it's", "that's", "there's", "what's", "here's", "let's", "who's", "where's"}:
            continue  # possessive
        yield m.group(0)


@rule("1.8", "'and/or'")
def and_or(s):
    for m in re.finditer(r"\band/or\b", s, re.I):
        yield m.group(0)


@rule("1.6", "Modal with unfixed meaning (lowercase should/might/could/would/may not)")
def modals(s):
    for m in re.finditer(r"\b(should|might|could|would|may not)\b", s):
        yield m.group(0)


@rule("1.9", "Connective with two meanings (since/as/once/while at clause start)")
def ambiguous_connectives(s):
    for m in re.finditer(r"(?:^|\s|\d+\.\s+)(Since|since)\b(?!\s+(?:version|v?\d|release|the release|January|February|March|April|May|June|July|August|September|October|November|December|then))", s):
        yield m.group(1)
    for m in re.finditer(r"(?:^|\d+\.\s+)(As|Once)\b(?!\s+(?:a result|an example|shown|described|mentioned|noted|follows|well as|of|per|soon as|needed|required))", s):
        yield m.group(1)
    for m in re.finditer(r",\s+(as)\s+(?:the|a|an|it|this|we|you|they)\b", s):
        yield m.group(0).lstrip(", ")
    for m in re.finditer(r",\s+(while)\s+(?:the|a|an|it|this|we|you|they|other|others|some)\b", s):
        yield m.group(0).lstrip(", ") + " (time or contrast?)"


@rule("1.10", "Latin abbreviation; write it in full")
def latin(s):
    for m in re.finditer(r"\b(?:e\.g\.|i\.e\.|etc\.|vs\.?|cf\.|viz\.)", s, re.I):
        yield m.group(0)


@rule("1.10", "Idiom or figure of speech")
def idioms(s):
    idiom_list = [
        "up and running", "out of the box", "under the hood", "on the fly", "rule of thumb",
        "touch base", "heads up", "heads-up", "low-hanging fruit", "move the needle",
        "circle back", "in a nutshell", "a piece of cake", "on the same page", "ballpark",
        "deep dive", "deep-dive", "keep in mind", "bear in mind", "at the end of the day",
        "game changer", "game-changer", "silver bullet", "out of the loop", "in the loop",
        "behind the scenes", "under the radar", "hit the ground running", "boil the ocean",
        "sweet spot", "bells and whistles", "rabbit hole", "on the back burner", "take a look",
        "have a look", "get the ball rolling", "out of sync", "first-class citizen",
        "batteries included", "happy path", "sanity check", "plays nicely", "plays well",
    ]
    low = s.lower()
    for idiom in idiom_list:
        if re.search(rf"\b{re.escape(idiom)}\b", low):
            yield idiom


@rule("3.5", "WH-question")
def wh_question(s):
    if s.strip().endswith("?") and re.match(r"\s*(?:\d+\.\s*)?(what|which|where|when|why|how|who)\b", s, re.I):
        yield s.strip()[:40]


@rule("2.1", "Imperative without determiner (telegraphic style)")
def no_determiner(s):
    m = re.match(rf"\s*(?:\d+\.\s*)?({IMPERATIVE_VERBS})\s+([a-z][a-z-]+)\b", s)
    if not m:
        return
    nxt = m.group(2)
    if nxt in DETERMINERS or nxt.endswith("ly"):
        return
    if nxt in {"to", "in", "on", "from", "with", "for", "at", "into", "if", "and", "or", "it", "them", "up", "out", "down", "off", "back", "over", "by", "through", "until", "when", "as"}:
        return
    yield m.group(0).strip()


@rule("3.9", "Long sentence (over 25 words); check for scope and attachment ambiguity")
def long_sentence(s):
    words = re.findall(r"[A-Za-z0-9'’±.-]+", s)
    if len(words) > 25:
        yield f"{len(words)} words"


@rule("5.5", "Semicolon or clause-joining dash; prefer two sentences")
def semicolon(s):
    if ";" in s:
        yield ";"
    if re.search(r"\w\s+[-–—]\s+\w", s) or re.search(r"\w—\w", s):
        yield "dash"


# ---------------------------------------------------------------- preprocessing

def preprocess(text, check_tables=False):
    """Return a list of prose lines with code, URLs and markup neutralised."""
    lines_out = []
    in_fence = False
    fence = None
    for raw in text.splitlines():
        stripped = raw.strip()
        fm = re.match(r"^(```+|~~~+)", stripped)
        if fm:
            if not in_fence:
                in_fence, fence = True, fm.group(1)[0] * 3
            elif stripped.startswith(fence):
                in_fence = False
            continue
        if in_fence:
            continue
        if not stripped:
            lines_out.append("")
            continue
        if re.match(r"^ {4,}\S", raw) or raw.startswith("\t"):  # indented code
            if not re.match(r"^\s*(?:[-*+]|\d+\.)\s", raw):
                continue
        if stripped.startswith("#"):  # heading: titles may be fragments
            continue
        if stripped.startswith("|") or re.match(r"^:?-{3,}:?(\s*\|\s*:?-{3,}:?)*$", stripped):
            if not check_tables:
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            for c in cells:
                if c and not re.match(r"^:?-+:?$", c):
                    lines_out.append(c)
            continue
        line = stripped
        line = re.sub(r"<[^>]+>", " ", line)                                 # HTML tags
        line = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", line)                     # images
        line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)                  # links -> text
        line = re.sub(r"``[^`]+``|`[^`]+`", "CODE", line)                     # inline code
        line = re.sub(r"https?://\S+|www\.\S+", "URL", line)                 # bare URLs
        line = re.sub(r"\*\*|__", "", line)                                   # bold
        line = re.sub(r"(?<!\w)[*_](?=\S)|(?<=\S)[*_](?!\w)", "", line)       # italics
        line = re.sub(r"^(?:>\s*)+", "", line)                                # blockquote
        line = re.sub(r"^\[!\w+\]\s*", "", line)                              # GitHub admonition
        line = re.sub(r"^[-*+]\s+(?:\[[ xX]\]\s+)?", "", line)                # bullets / tasks
        line = re.sub(r"\b(MUST NOT|SHALL NOT|SHOULD NOT|MUST|SHALL|SHOULD|MAY|REQUIRED|RECOMMENDED|OPTIONAL)\b", "RFC", line)
        if line.strip():
            lines_out.append(line.strip())
    return lines_out


def split_sentences(lines):
    sentences = []
    for line in lines:
        if not line:
            continue
        protected = re.sub(r"\b(e\.g|i\.e|etc|vs|cf|viz)\.", lambda m: m.group(0).replace(".", "§"), line, flags=re.I)
        protected = re.sub(r"(\d)\.(\d)", r"\1§\2", protected)
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(]|CODE|URL)", protected):
            s = s.replace("§", ".").strip()
            if s and re.search(r"[A-Za-z]", s):
                sentences.append(s)
    return sentences


def check(text, check_tables=False):
    findings = []
    for idx, sentence in enumerate(split_sentences(preprocess(text, check_tables)), 1):
        for rule_id, desc, fn in RULES:
            for hit in fn(sentence):
                findings.append({"sentence_no": idx, "rule": rule_id, "issue": desc,
                                 "match": hit, "sentence": sentence})
    return findings


def main(argv):
    as_json = "--json" in argv
    tables = "--tables" in argv
    args = [a for a in argv if a not in ("--json", "--tables")]
    text = open(args[0], encoding="utf-8").read() if args else sys.stdin.read()
    findings = check(text, tables)
    if as_json:
        print(json.dumps(findings, indent=2))
        return
    if not findings:
        print("No pattern-level issues found. Still review terms, antecedents and attachment by reading.")
        return
    current = None
    for f in findings:
        if f["sentence_no"] != current:
            current = f["sentence_no"]
            print(f"\n[{current}] {f['sentence']}")
        print(f"   rule {f['rule']}: {f['issue']}  ->  \"{f['match']}\"")
    print(f"\n{len(findings)} flag(s). Rule numbers refer to references/rules.md. "
          "CODE = inline code, URL = link, RFC = RFC 2119 keyword (not checked).")


if __name__ == "__main__":
    main(sys.argv[1:])

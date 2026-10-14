"""
Shared helpers for the Bible Games pages.

Answer checking lives here because several games ask the player to type a
Bible name, and the matching rules are subtle enough that they should exist
in exactly one place.
"""

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent


def load_json(filename, key):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)[key]


def normalize(text):
    """
    Strip case, punctuation, leading articles and extra spaces so that
    "St. Paul!" and "paul" compare equal.
    input: text --> str
    output: str
    """
    cleaned = re.sub(r"[^a-z0-9 ]", " ", text.lower())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return re.sub(r"^(the|saint|st) ", "", cleaned)


def accepted_names(entry, answer_key="answer"):
    names = [normalize(name) for name in entry.get("accept", [])]
    names.append(normalize(entry[answer_key]))
    return [name for name in names if name]


def build_name_index(entries, answer_key="answer"):
    """
    Map every accepted name to the entries that own it, so a guess naming a
    different character is never excused as a typo. Some names are
    deliberately shared, such as Saul for both Saul and Paul.
    input: entries --> list of dict, answer_key --> str
    output: dict of str -> set of answer strings
    """
    index = {}
    for entry in entries:
        for name in accepted_names(entry, answer_key):
            index.setdefault(name, set()).add(entry[answer_key])
    return index


def edit_distance(first, second, limit):
    """
    Levenshtein distance, giving up early once it cannot land within limit.
    input: first --> str, second --> str, limit --> int
    output: int
    """
    if abs(len(first) - len(second)) > limit:
        return limit + 1

    previous = list(range(len(second) + 1))
    for i, letter in enumerate(first, start=1):
        current = [i]
        for j, other in enumerate(second, start=1):
            current.append(min(
                previous[j] + 1,
                current[j - 1] + 1,
                previous[j - 1] + (letter != other)
            ))
        if min(current) > limit:
            return limit + 1
        previous = current
    return previous[-1]


def typo_allowance(name):
    """
    How many wrong letters to forgive. Short names get none, because one
    letter is all that separates Saul from Paul or Mary from Mara.
    input: name --> str
    output: int
    """
    if len(name) >= 9:
        return 2
    if len(name) >= 6:
        return 1
    return 0


def is_correct(guess, entry, name_index, answer_key="answer"):
    """
    Check a guess against every accepted spelling of the answer, forgiving
    small typos on longer names only.
    input: guess --> str, entry --> dict, name_index --> dict, answer_key --> str
    output: bool
    """
    attempt = normalize(guess)
    if not attempt:
        return False

    accepted = accepted_names(entry, answer_key)
    if attempt in accepted:
        return True

    # An exact name belonging only to someone else is a wrong answer, never a typo.
    owners = name_index.get(attempt)
    if owners and entry[answer_key] not in owners:
        return False

    for name in accepted:
        allowance = typo_allowance(name)
        if allowance and edit_distance(attempt, name, allowance) <= allowance:
            return True
    return False

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


WORD_RE = re.compile(r"[A-Za-z0-9À-ÿ]+(?:['’-][A-Za-z0-9À-ÿ]+)?")
HASHTAG_RE = re.compile(r"(#\w+)")
MENTION_RE = re.compile(r"(@[A-Za-z0-9._]+)")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_text(value: Any) -> str:
    text = str(value or "")
    return " ".join(text.split()).strip()


def extract_words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def evaluate_text(value: Any) -> tuple[str, int, bool, str]:
    clean_text = normalize_text(value)
    if not clean_text:
        return "", 0, False, "empty_text"

    words = extract_words(clean_text)
    word_count = len(words)
    has_alpha = any(any(char.isalpha() for char in word) for word in words)

    if not has_alpha:
        return clean_text, word_count, False, "nonalpha_or_emoji_only"
    if word_count < 3:
        return clean_text, word_count, False, "less_than_3_words"

    return clean_text, word_count, True, ""


def parse_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def parse_bool(value: Any) -> str:
    return "true" if bool(value) else "false"


def parse_iso(value: Any) -> str:
    return normalize_text(value)


def serialize_list(items: list[str]) -> str:
    return "|".join(items)


def extract_hashtags(text: Any) -> list[str]:
    return HASHTAG_RE.findall(normalize_text(text))


def extract_mentions(text: Any) -> list[str]:
    return MENTION_RE.findall(normalize_text(text))

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GENERIC_SHORT_TEXT = {
    "ok",
    "oke",
    "mantap",
    "nice",
    "bagus",
    "good",
    "great",
}

WORD_RE = re.compile(r"\b[\w'-]+\b", flags=re.UNICODE)
ALPHA_RE = re.compile(r"[A-Za-zÀ-ÿ]")
EMOJI_OR_SYMBOL_ONLY_RE = re.compile(r"^[\W_]+$", flags=re.UNICODE)


@dataclass(slots=True)
class TextCheckResult:
    raw_text: str
    clean_text: str
    word_count: int
    is_valid: bool
    filter_reason: str


def ensure_parent(path: str | Path) -> Path:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path


def load_records(path: str | Path) -> list[dict[str, Any]]:
    input_path = Path(path)
    suffix = input_path.suffix.lower()
    if suffix == ".json":
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        if isinstance(payload, dict):
            if isinstance(payload.get("items"), list):
                return [item for item in payload["items"] if isinstance(item, dict)]
            return [payload]
    if suffix in {".csv", ".tsv"}:
        import pandas as pd

        sep = "\t" if suffix == ".tsv" else ","
        return pd.read_csv(input_path, sep=sep).to_dict(orient="records")
    raise ValueError(f"Unsupported input format: {input_path}")


def write_csv(rows: list[dict[str, Any]], output_path: str | Path) -> None:
    import pandas as pd

    df = pd.DataFrame(rows)
    ensure_parent(output_path)
    df.to_csv(output_path, index=False)


def pick_first(record: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = record.get(key)
        if value not in (None, "", [], {}):
            return value
    return None


def parse_date(value: Any) -> str | None:
    if value in (None, ""):
        return None
    import dateparser

    dt = dateparser.parse(str(value))
    if not dt:
        return None
    return dt.isoformat()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_text(text: str | None) -> str:
    if text is None:
        return ""
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def has_sentence_signal(text: str) -> bool:
    if len(text) >= 20:
        return True
    if any(mark in text for mark in [".", ",", "!", "?", ";", ":"]):
        return True
    return count_words(text) >= 4


def evaluate_text(text: str | None, min_words: int = 3, min_chars: int = 12) -> TextCheckResult:
    clean = normalize_text(text)

    if not clean:
        return TextCheckResult("", "", 0, False, "empty_text")

    if not ALPHA_RE.search(clean):
        return TextCheckResult(clean, "", 0, False, "emoji_or_symbol_only")

    word_count = count_words(clean)
    if word_count < min_words:
        return TextCheckResult(clean, "", word_count, False, "too_short_word_count")

    if len(clean) < min_chars:
        return TextCheckResult(clean, "", word_count, False, "too_short_character_count")

    if clean.lower() in GENERIC_SHORT_TEXT:
        return TextCheckResult(clean, "", word_count, False, "generic_short_text")

    if EMOJI_OR_SYMBOL_ONLY_RE.match(clean):
        return TextCheckResult(clean, "", word_count, False, "emoji_or_symbol_only")

    if not has_sentence_signal(clean):
        return TextCheckResult(clean, "", word_count, False, "no_sentence_signal")

    return TextCheckResult(clean, clean, word_count, True, "")


def extract_hashtags(text: str | None) -> list[str]:
    return re.findall(r"#(\w+)", normalize_text(text))


def extract_mentions(text: str | None) -> list[str]:
    return re.findall(r"@(\w+)", normalize_text(text))

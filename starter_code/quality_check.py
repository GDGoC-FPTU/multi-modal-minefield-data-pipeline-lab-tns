# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

import re


TOXIC_PATTERNS = [
    re.compile(r"null\s*pointer\s*exception", re.IGNORECASE),
    re.compile(r"traceback\s*\(most recent call last\)", re.IGNORECASE),
    re.compile(r"\b(segmentation fault|fatal error|stack trace)\b",
               re.IGNORECASE),
]


def _remove_toxic_strings(text):
    cleaned = text
    for pattern in TOXIC_PATTERNS:
        cleaned = pattern.sub(" ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def _has_numeric_rule_discrepancy(text):
    # Detect contradictory percentage claims in close context, e.g. "8%" vs "10%".
    lowered = text.lower()
    if not any(keyword in lowered for keyword in ("tax", "vat", "thu", "rule", "logic")):
        return False

    percentages = set(re.findall(r"(\d{1,2})\s*%", lowered))
    return len(percentages) > 1


def run_quality_gate(document_dict):
    if not isinstance(document_dict, dict):
        return False

    content = document_dict.get("content")
    if not isinstance(content, str):
        return False

    cleaned_content = _remove_toxic_strings(content)
    document_dict["content"] = cleaned_content

    # Reject near-empty payloads after cleanup.
    if len(cleaned_content) < 20:
        return False

    metadata = document_dict.get("source_metadata")
    metadata_text = ""
    if isinstance(metadata, dict):
        metadata_text = " ".join(str(v)
                                 for v in metadata.values() if v is not None)

    combined_text = f"{cleaned_content} {metadata_text}".strip()
    if _has_numeric_rule_discrepancy(combined_text):
        return False

    return True

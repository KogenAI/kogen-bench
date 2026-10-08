"""Shared detection and redaction for private filesystem/archive locations."""
import re


_PRIVATE_FORMS = (
    re.compile(r"/" + "srv" + r"/"),
    re.compile(r"<" + "HOME" + r">"),
    re.compile(r"\bre" + "covery-" + r"\d{4}-\d{2}-\d{2}/levers/"),
)
_REDACTIONS = (
    (re.compile(r"/" + "srv" + r"/[^\s\"'`<>),;]+"), "public-source-location-withheld"),
    (re.compile(r"<" + "HOME" + r">(?:/[^\s\"'`<>),;]+)?"), "public-base-location-withheld"),
    (re.compile(r"\bre" + "covery-" + r"\d{4}-\d{2}-\d{2}/levers/[^\s\"'`<>),;]*"), "public-source-location-withheld"),
)


def contains_private_path(value):
    """Return true for private absolute paths and dated recovery archive paths."""
    return isinstance(value, str) and any(pattern.search(value) for pattern in _PRIVATE_FORMS)


def redact_private_paths(value):
    """Replace private path forms while preserving surrounding public metadata."""
    if not isinstance(value, str):
        return value
    for pattern, replacement in _REDACTIONS:
        value = pattern.sub(replacement, value)
    return value

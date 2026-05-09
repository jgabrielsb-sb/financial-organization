import unicodedata


def normalize_name(name: str) -> str:
    """Strip, uppercase, and remove accent marks while preserving cedilla (ç → Ç)."""
    name = name.strip().upper()
    decomposed = unicodedata.normalize("NFD", name)
    filtered = "".join(
        c for c in decomposed
        if unicodedata.category(c) != "Mn" or c == "̧"
    )
    return unicodedata.normalize("NFC", filtered)

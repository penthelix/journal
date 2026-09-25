def sanitize_text(unsanitized_input: str) -> str:
    return "".join(
        c if c.isalnum() or c in ("-", "_") else "_" for c in unsanitized_input
    )

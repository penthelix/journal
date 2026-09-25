def sanitize_text(unsanitized_input: str, strict: bool = True) -> str:
    if not strict:
        return "".join(
            c
            if c.isalnum() or c in ("-", "_", "(", ")", ",", ".", "`", "'", '"', " ")
            else "_"
            for c in unsanitized_input
        )
    return "".join(
        c if c.isalnum() or c in ("-", "_") else "_" for c in unsanitized_input
    )

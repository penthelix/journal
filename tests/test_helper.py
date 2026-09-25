from journal.helper import sanitize_text


def test_sanitize_text():
    test_unsanitized_text = "thequickbrownfoxjumpsoverthelazydogTHEQUICKBROWNFOXJUMPSOVERTHELAZYDOG0123456789-_(),.`'\" <>[];:"
    expected_sanitized_text_strict = "thequickbrownfoxjumpsoverthelazydogTHEQUICKBROWNFOXJUMPSOVERTHELAZYDOG0123456789-_______________"
    expected_sanitized_text_not_strict = "thequickbrownfoxjumpsoverthelazydogTHEQUICKBROWNFOXJUMPSOVERTHELAZYDOG0123456789-_(),.`'\" ______"
    assert (
        sanitize_text(test_unsanitized_text, strict=True)
        == sanitize_text(test_unsanitized_text)
        == expected_sanitized_text_strict
    )
    assert (
        sanitize_text(test_unsanitized_text, strict=False)
        == expected_sanitized_text_not_strict
    )

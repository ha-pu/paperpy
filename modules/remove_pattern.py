def remove_pattern(text):
    """
    This function checks if the input text starts with the pattern "```html"
    and/or ends with the pattern "```".
    If these patterns are found, they are removed from the text.
    Args:
        text (str): The input text from which the patterns are to be removed.
    Returns:
        str: The text with the specified patterns removed from the beginning and/or end.
    """
    pattern_start = "```html"
    pattern_end = "```"
    if text.startswith(pattern_start):
        text = text[len(pattern_start):]
    if text.endswith(pattern_end):
        text = text[:-len(pattern_end)]
    return text
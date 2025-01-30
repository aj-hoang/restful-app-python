import re


def clean_genre(input: str) -> str:
    # Trim, lower
    input_lower_strip = input.lower().strip()

    # remove double spaces with single space
    input_spaces_trimmed = re.sub("[ ]+", " ", input_lower_strip)

    # remove special characters from string - could be improved to keep characters with accents etc..
    cleaned_input = re.sub("[^A-Za-z ]", "", input_spaces_trimmed)
    return cleaned_input

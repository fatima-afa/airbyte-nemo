import re


def to_snake_case(s):
    # Replace all non-alphanumeric characters with spaces
    s = re.sub(r'\W+', ' ', s)
    # Convert to lower case and split the string into words
    words = s.lower().split()
    # Join words using underscore
    return '_'.join(words)

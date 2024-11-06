#!/usr/bin/env python3
"""Module for personal data project
"""

import re
from typing import List

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
) -> str:
    """Returns the log message with certain fields obfuscated.

    Args:
        fields (List[str]): a list of strings representing all fields to
        obfuscate.
        redaction (str): a string representing by what the field will be
        obfuscated.
        message (str): a string representing the log line.
        separator (str): a string representing by which character is separating
        all fields in the log line (message).

    Returns:
        str: the log message obfuscated.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)

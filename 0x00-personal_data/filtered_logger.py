#!/usr/bin/env python3
"""Module for personal data project
"""

import logging
import re
from typing import List

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

# Tuple of PII fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class

    Update the class to accept a list of strings fields constructor argument.
    Implement the format method to filter values in incoming log records using
    filter_datum. Values for fields in fields should be filtered.
    DO NOT extrapolate FORMAT manually. The format method should be less than
    5 lines long.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the class.

        Args:
            fields (List[str]): The fields.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum.

        Args:
            record (logging.LogRecord): A logging.LogRecord instance.

        Returns:
            str: A string with all occurrences of the `self.fields` in
            `record.message` replaced by the `self.REDACTION` string.
        """
        # Call the parent class's format method to get the formatted log line
        msg = super(RedactingFormatter, self).format(record)
        # Use the filter_datum function to perform substitution of self.fields
        text = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return text


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


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object named "user_data".

    The logger should be named "user_data" and only log up to logging.INFO
    level.
    It should not propagate messages to other loggers. It should have a
    StreamHandler with RedactingFormatter as formatter.
    Create a tuple PII_FIELDS constant at the root of the module containing
    the fields from user_data.csv that are considered PII. PII_FIELDS can
    contain only 5 fields - choose the right list of fields that can are
    considered as “important” PIIs or information that you must hide in your
    logs. Use it to parameterize the formatter.

    Returns:
        logging.Logger: A logging.Logger instance.
    """
    # Create a logger with the specified name
    logger = logging.getLogger("user_data")
    # Set the logging level to only log messages up to logging.INFO
    logger.setLevel(logging.INFO)
    # Create a StreamHandler to output log messages to the console
    stream_handler = logging.StreamHandler()
    # Disable propagation of log messages to other loggers
    logger.propagate = False
    # Create an instance of the RedactingFormatter class with the PII_FIELDS,
    # as fields and set the formatter of the handler
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    # Add the handler to the logger
    logger.addHandler(stream_handler)
    return logger
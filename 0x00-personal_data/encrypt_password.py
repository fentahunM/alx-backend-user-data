#!/usr/bin/env python3
"""Module for encrypting passwords.
"""

import logging
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the provided password using bcrypt.
    """
    # Salt and hash the password using the bcrypt package
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validates the provided password matches the hashed password """
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
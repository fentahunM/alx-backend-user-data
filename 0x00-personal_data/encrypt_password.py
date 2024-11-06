#!/usr/bin/env python3
"""Module for encrypting passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the provided password using bcrypt.
    """
    # Salt and hash the password using the bcrypt package
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

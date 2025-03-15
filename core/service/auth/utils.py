import hashlib

from core import config


def make_password(password):
    salt = hashlib.sha256(config.SECRET_KEY.encode("utf-8")).hexdigest()

    password_salt = password + salt

    password_hash = hashlib.sha256(password_salt.encode("utf-8")).hexdigest()

    return password_hash


def is_valid_password(stored_hash, password):
    salt = hashlib.sha256(config.SECRET_KEY.encode("utf-8")).hexdigest()

    password_salt = password + salt

    password_hash = hashlib.sha256(password_salt.encode("utf-8")).hexdigest()

    return password_hash == stored_hash

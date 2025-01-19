import bcrypt


def hash_password(to_hash: str) -> str:
    salt = bcrypt.gensalt()
    bytes = to_hash.encode("utf-8")

    return bcrypt.hashpw(bytes, salt)

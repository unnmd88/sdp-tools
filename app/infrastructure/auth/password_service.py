import bcrypt


class BcryptPasswordService:
    @classmethod
    def hash_password(cls, password: str) -> bytes:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        )

    @classmethod
    def verify_password(cls, *, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=hashed_password,
        )



def hash_password(
    password: str,
) -> bytes:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )


from passlib.context import CryptContext

class PasswordHelper:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self):
        pass

    @classmethod
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    @classmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

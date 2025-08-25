import bcrypt

class BcryptPasswordHasher:
    def __call__(self, raw: str) -> str:
        return self.hash(raw)
    def hash(self, raw: str) -> str:
        return bcrypt.hashpw(raw.encode(), bcrypt.gensalt()).decode()

    def verify(self, stored_hash: str, raw: str) -> bool:
        try:
            return bcrypt.checkpw(raw.encode(), stored_hash.encode())
        except ValueError:
            return False

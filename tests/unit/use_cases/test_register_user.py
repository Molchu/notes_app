import pytest

from application.use_cases.register_user import RegisterUser
from core.entities.user import User
from core.value_objects.email import Email
from core.exceptions import DomainError


# ---------- Fakes ----------
class InMemoryUserRepo:
    def __init__(self):
        self._by_id = {}
        self._by_email = {}
        self._auto_id = 1

    def add(self, user: User) -> User:
        uid = self._auto_id
        self._auto_id += 1
        stored = User(
            id=uid,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash
        )
        self._by_id[uid] = stored
        self._by_email[user.email.value] = stored
        return stored

    def get_by_email(self, email: Email):
        return self._by_email.get(email.value)

    # opcional para otros tests
    def get_by_id(self, uid: int):
        return self._by_id.get(uid)


def simple_hasher(raw: str) -> str:
    return f"hash:{raw}"


# ---------- Tests ----------
def test_register_user_success():
    repo = InMemoryUserRepo()
    use_case = RegisterUser(user_repo=repo, password_hasher=simple_hasher)

    user = use_case.execute(username="nicolas", email="nico@test.com", raw_password="1234")

    assert user.id == 1
    assert user.username == "nicolas"
    assert user.email.value == "nico@test.com"
    assert user.password_hash == "hash:1234"


def test_register_user_duplicate_email_raises_domain_error():
    repo = InMemoryUserRepo()
    use_case = RegisterUser(user_repo=repo, password_hasher=simple_hasher)

    use_case.execute(username="nico", email="nico@test.com", raw_password="1234")

    with pytest.raises(DomainError):
        use_case.execute(username="otro", email="nico@test.com", raw_password="abcd")

import pytest

from application.use_cases.login_user import LoginUser
from core.entities.user import User
from core.value_objects.email import Email
from core.exceptions import DomainError


# ---------- Fakes ----------
class InMemoryUserRepo:
    def __init__(self):
        self._by_email = {}

    def seed(self, user: User):
        self._by_email[user.email.value] = user

    def get_by_email(self, email: str | Email):
        if isinstance(email, Email):
            key = email.value
        else:
            key = email
        return self._by_email.get(key)


def password_checker(stored_hash: str, raw: str) -> bool:
    # valida formato "hash:<raw>"
    return stored_hash == f"hash:{raw}"


# ---------- Tests ----------
def test_login_success():
    repo = InMemoryUserRepo()
    user = User(id=10, username="nicolas", email=Email("nico@test.com"), password_hash="hash:1234")
    repo.seed(user)

    use_case = LoginUser(user_repo=repo, password_checker=password_checker)
    logged = use_case.execute(email="nico@test.com", raw_password="1234")

    assert logged.id == 10
    assert logged.username == "nicolas"


def test_login_user_not_found():
    repo = InMemoryUserRepo()
    use_case = LoginUser(user_repo=repo, password_checker=password_checker)

    with pytest.raises(DomainError):
        use_case.execute(email="no@existe.com", raw_password="x")


def test_login_wrong_password():
    repo = InMemoryUserRepo()
    user = User(id=11, username="nicolas", email=Email("nico@test.com"), password_hash="hash:correcta")
    repo.seed(user)
    use_case = LoginUser(user_repo=repo, password_checker=password_checker)

    with pytest.raises(DomainError):
        use_case.execute(email="nico@test.com", raw_password="incorrecta")

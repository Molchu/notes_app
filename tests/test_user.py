import pytest
from core.entities.user import User
from core.value_objects.email import Email

def fake_password_checker(stored_hash, raw):
    return stored_hash == f"hash:{raw}"

def test_create_user_valid():
    user = User(
        id=1,
        username="nicolas",
        email=Email("nico@test.com"),
        password_hash="hash:1234"
    )
    assert user.username == "nicolas"
    assert user.check_password("1234", fake_password_checker) is True

def test_invalid_username():
    with pytest.raises(ValueError):
        User(id=2, username="a", email=Email("a@a.com"), password_hash="hash:pw")
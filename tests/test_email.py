import pytest
from core.value_objects.email import Email
from core.exceptions import DomainValidationError

def test_valid_email():
    e = Email("Test@Domain.com")
    assert str(e) == "test@domain.com"
    assert e.local == "test"
    assert e.domain == "domain.com"

def test_invalid_email_format():
    with pytest.raises(DomainValidationError):
        Email("bademail")

def test_email_masked():
    e = Email("julio@example.com")
    masked = e.masked()
    assert masked.startswith("ju") and masked.endswith("@example.com")

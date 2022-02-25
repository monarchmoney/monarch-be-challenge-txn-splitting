import pytest

from monarch.db.models import User

pytestmark = pytest.mark.usefixtures("db")


def test_create_user():
    email = 'foo@gmail.com'
    user = User.objects.create(email='foo@gmail.com', password='password')
    assert user.email == email

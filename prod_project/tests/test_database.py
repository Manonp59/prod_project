import pytest
from main.models import User


@pytest.mark.django_db
def test_connexion():
    all_object = User.objects.all()
    assert all_object is not None

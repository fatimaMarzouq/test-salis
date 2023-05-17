import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproject.settings')

django.setup()
from testapp.models import Flower
import pytest


@pytest.fixture(name="flower")
def create_flower():
    """Create a merchant instance."""
    return Flower.objects.create(
        name="flower",
        type="plants",
    )


def test_capture_payment_model(flower):
    """Test capture payment model."""
    assert flower.name == "flower"
    assert flower.type == "plants"

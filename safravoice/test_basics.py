import pytest

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safraapp.settings')
print(os.environ.get('DJANGO_SETTINGS_MODULE'))
import django
django.setup()
from safravoice.models import ReqBuilder


# Create your tests here.
def test_security_chave():
    result = ReqBuilder.objects.filter(description='Requisição de token')
    assert result.get(
    ).url == 'https://idcs-902a944ff6854c5fbe94750e48d66be5.identity.oraclecloud.com/oauth2/v1/token'

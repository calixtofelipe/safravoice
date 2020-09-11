import pytest

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safraapp.settings')
print(os.environ.get('DJANGO_SETTINGS_MODULE'))
import django
django.setup()
from safravoice.models import Security


# Create your tests here.
def test_security_chave():
    result = Security.objects.filter(chave='client_id')
    assert result.get().valor == 'xpto'

from cryptography.fernet import Fernet
from django.conf import settings


def encrypt(data):
    f = Fernet(settings.CRYPT_KEY)
    return f.encrypt(data)


def decrypt(data):
    f = Fernet(settings.CRYPT_KEY)
    return f.decrypt(data)

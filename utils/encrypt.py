import hashlib
from django.conf import settings


def md5(data_string):
    salt_str = settings.SECRET_KEY.encode("utf-8")
    obj = hashlib.md5(salt_str)
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()

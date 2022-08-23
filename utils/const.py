# -*- coding: UTF-8 -*-
from enum import Enum


class Role(str, Enum):
    ADMIN = "1"
    CUSTOMER = "2"

    def __str__(self):
        return self.value


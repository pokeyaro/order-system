# -*- coding: UTF-8 -*-

class BaseResponse(object):
    """ 统一的返回对象格式 """
    def __init__(self):
        self.status = False
        self.detail = None
        self.data = None

    @property
    def dict(self):
        return self.__dict__

from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class UserInfo(object):
    def __init__(self, role, name, id):
        self.name = name
        self.role = role
        self.id = id


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """ 校验用户是否已登录 """
        # 1.不需要登录就可以访问的URL
        if request.path_info in settings.MY_WHITE_URL:
            return None

        # 2.session中获取用户信息, 能获取到登录成功
        user_dict = request.session.get(settings.MY_SESSION_KEY)

        # 3.未登录, 跳转回登录页面
        if not user_dict:
            return redirect(settings.MY_LOGIN_URL)

        # 4.已登录, 封装用户信息（方便后续用到已登录的用户信息）
        request.login_user = UserInfo(**user_dict)
        return None


    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass


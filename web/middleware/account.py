from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin


class UserInfo(object):
    def __init__(self, role, name, id):
        self.name = name
        self.role = role
        self.id = id
        self.menu_name = None
        self.crumbs_list = None


class AuthMiddleware(MiddlewareMixin):

    def white_url_access(self, request):
        """ 白名单是否放行 """
        if request.path_info in settings.MY_WHITE_URL:
            return True

    def process_request(self, request):
        """ 校验用户是否已登录 """
        # 1.无需登录即可访问的URL
        if self.white_url_access(request):
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
        """ 校验用户URL的访问权限 """
        # 1.无需登录即可访问的URL
        if self.white_url_access(request):
            return None

        # 2.是否为公共的权限
        current_name = request.resolver_match.url_name
        if current_name in settings.MY_PERMISSION_PUBLIC:
            return None

        # 3.根据用户角色获取自己具备所有的权限
        user_permission_dict = settings.MY_PERMISSION[request.login_user.role]

        # 4.获取当前用户访问的URL
        current_name = request.resolver_match.url_name

        # 5.判断是否在自己具备的权限
        if current_name not in user_permission_dict:
            return render(request, "no_perms.html")

        # 6.有权限, 子uri可进入（向上寻找是否parent为None）, 面包屑路径导航
        text_list = list()
        current_text = user_permission_dict[current_name]['text']
        text_list.append(current_text)

        url_list = list()
        try:
            # 固定url
            current_url = reverse(current_name)
        except:
            # 动态url
            current_url = request.path_info
        url_list.append(current_url)

        menu_name = current_name
        while user_permission_dict[menu_name]['parent']:
            menu_name = user_permission_dict[menu_name]['parent']

            level_text = user_permission_dict[menu_name]['text']
            text_list.append(level_text)

            level_url = reverse(menu_name)
            url_list.append(level_url)

        text_list.append("首页")
        url_list.append("/home/")
        text_list.reverse()
        url_list.reverse()

        # 6.1 当前菜单的值
        request.login_user.menu_name = menu_name

        # 6.2 路径导航list (text: url)
        request.login_user.crumbs_list = list(zip(text_list, url_list))
        return None

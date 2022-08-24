import copy

from django.conf import settings
from django.template import Library

register = Library()


@register.inclusion_tag("tag/my_menu.html")
def my_menu(request):
    # 1.当前用户的角色信息
    login_role = request.login_user.role

    # 2.菜单信息
    user_menu_list = copy.deepcopy(settings.MY_MENU.get(login_role))
    # 默认选中处理（可控制其他菜单栏默认收缩隐藏）
    for item in user_menu_list:
        # item['class'] = 'visually-hidden'
        for child in item['children']:
            # if child['url'] == request.path_info:                 # v1版本
            if child['name'] == request.login_user.menu_name:       # v2版本
                child['class'] = 'active'
                # item['class'] = ''

    return {'menu_list': user_menu_list}

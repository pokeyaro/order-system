from django.template import Library
from django.conf import settings

register = Library()


@register.inclusion_tag("tag/my_menu.html")
def my_menu(requests):
    # 1.当前用户的角色信息
    login_role = requests.login_user.role

    # 2.菜单信息
    user_menu_list = settings.MY_MENU.get(login_role)

    return {'menu_list': user_menu_list}

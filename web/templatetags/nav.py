from django.conf import settings
from django.template import Library

register = Library()


@register.inclusion_tag("tag/my_nav.html")
def my_nav(request):
    if request.path_info == settings.MY_LOGIN_HOME:
        return {}

    # 1.当前用户的角色信息
    crumbs_list = request.login_user.crumbs_list

    # if request.path_info not in crumbs_list:
    #     print(request.path_info)
    #     print(crumbs_list)
    #     return {}

    # 2.将dict中最后一对剔除掉
    current_list = crumbs_list.pop()

    # print(request.path_info)
    # print(request.resolver_match.url_name)
    return {'crumbs_list_pop_last': crumbs_list, 'current_text': current_list[0], 'current_url': current_list[1]}

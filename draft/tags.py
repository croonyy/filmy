from django import template
import json
# from rbac.models import RbacPermission
# from rbac.util.user_perms import get_user_perms
from django.http import JsonResponse
import logging

register = template.Library()

logger = logging.getLogger('ud_logger')


# @register.simple_tag(takes_context=True)
def get_menu(context):
    print('get_menu data...')
    request = context['request']
    # user = request.user
    if 0:
        pass
    # if user.is_superuser:
    #     queryset = RbacPermission.objects.filter(type='menu_perm').values()
    #     perm_list = list(queryset)
    #     for i in perm_list:
    #         i['perm_type'] = 'admin'
    #     permission_list_menu = perm_list
    else:
        try:
            # print('get_user_perms(request.user)')
            logger.info('get_user_perms(request.user)')
            permission_list = get_user_perms(request.user)
            # print('request.session.get("perm_list")')
            # permission_list = request.session.get("perm_list")
            if permission_list:
                permission_list_menu = [dic for dic in permission_list if dic['type'] == 'menu_perm']
            else:
                permission_list_menu = []
        except Exception as e:
            print("nav_data.py func[get_menu] error:" + str(e))
            permission_list_menu = []
        # print('get menu')
        # print(permission_list_menu)
        for dic in permission_list_menu:
            # if not dic['parent']:
            if not dic.get('parent_id'):
                dic['parent_id'] = 0
    return json.dumps(permission_list_menu)


@register.simple_tag(takes_context=True)
# @register.inclusion_tag(takes_context=True)
def get_perm_list(context):
    user = context['request'].user
    # return JsonResponse(get_user_perms(user))
    # return JsonResponse(get_user_perms(user), Dictsafe=False)
    return json.dumps(get_user_perms(user))
    # return get_user_perms(user)


@register.simple_tag(takes_context=True)
def get_cookie(context, cookie_id):
    # print("arg:"+cookie_id)
    request = context['request']
    result = request.COOKIES.get(cookie_id, '')
    # print('result:'+result)
    if result:
        return result
    else:
        return 'mn--max'


# @register.filter
# @register.simple_tag
# @register.inclusion_tag("rbac/test.html")
@register.simple_tag(takes_context=True)
def get_menu1(context, request):
    # return request
    permission_list = request.session.get("perm_list")
    per_list = []
    permission_dic = {}
    # 循环重构字典 ， 每一个权限的id 为键，新字典为value ，构成一个新的字典
    for per_dic in permission_list:
        new_per_dic = {}
        # 剔除非菜单权限
        if per_dic.get("type") == "url_perm":
            continue
        # 对菜单权限，重构数据结构，以id 值为键，新数据结构为value值
        new_per_dic["text"] = per_dic["title"]
        new_per_dic["href"] = per_dic["url"] or ""
        new_per_dic["pid"] = per_dic["parent_id"] or ""
        new_per_dic["nodes"] = []
        # new_per_dic["state"] = {"expanded":True} #此属性 设置节点展开 ，bootstrap_view 插件中的语法state :expanded为True 时节点时展开的
        permission_dic[per_dic.get("id")] = new_per_dic

    # 重构出的字典大致结构如下：
    # permission_dic={
    #     1:{"text":"信息管理","href":"","nodes":[],"pid":None},
    #     2:{"text":"权限管理","href":"","nodes":[],"pid":None},
    #     3:{"text":"客户管理","href":"","nodes":[],"pid":1},
    #     4:{"text":"订单管理","href":"","nodes":[],"pid":1},
    #     6:{"text":"查看客户","href":"","nodes":[],"pid":3},
    #     7:{"text":"查看订单","href":"","nodes":[],"pid":4},
    # }
    # 路径展开
    current_path = request.path

    # 过滤出一级权限，也就是 父pid 为None 的权限 ，加入已经准备好的数据列表
    for id, dic in permission_dic.items():
        # 找到根节点，也就是一级权限
        if not dic["pid"]:
            per_list.append(dic)
        else:
            permission_dic[dic["pid"]]["nodes"].append(dic)

        # 路径展开逻辑
        if dic["href"] == current_path:  # 找到当前的路径
            pid = dic["pid"]  # 找到当前路径的父级 pid
            # 通过while 循环不断的往上找父及诶单，并将父节点设置 相关的属性

            while pid:
                permission_dic[pid]["state"] = {"expanded": True}
                pid = permission_dic[pid]["pid"]
    # 为什么需要用json格式的，因为python代码 None,Ture 在js 语法中不能识别，所以需要转化成json字符串给插件
    # return {"default_data": json.dumps(per_list)}
    return json.dumps(permission_list)

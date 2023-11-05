# from application.ninja_cof import api
# Author 臧成龙
# coding=utf-8
# @Time    : 2022/5/19 21:36
# @File    : role.py
# @Software: PyCharm
# @qq: 939589097

from typing import List

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from system.models import Menu, Role, MenuButton, Dept, Users
from utils.fu_crud import create, delete, retrieve
from utils.fu_ninja import FuFilters, MyPagination
from utils.fu_response import FuResponse
from utils.list_to_tree import list_to_tree

router = Router()


class Filters(FuFilters):
    name: str = Field(None, alias="name")
    status: bool = Field(None, alias="status")
    id: str = Field(None, alias="id")


class SchemaIn(ModelSchema):
    menu: list = []
    permission: list = []
    dept: list = []
    column: list = []
    user: list = []

    class Config:
        model = Role
        model_exclude = ['id', 'dept', 'menu', 'permission', 'column', 'create_datetime', 'update_datetime']


class SchemaOut(ModelSchema):
    class Config:
        model = Role
        model_fields = "__all__"
    user: List[int] = []  # 该角色下所有用户id

    @staticmethod
    def resolve_user(obj):
        try:
            ret = []
            users = Users.objects.filter(role__id=obj.id).values()
            if len(users) >0:
                # TODO 注意这里有特殊处理：用户id要加一百万，部门id不用
                user_ids = [user.get('id')+1000000 for user in list(users)]
                ret += user_ids
            if len(obj.dept.all()) > 0:
                dept = obj.dept.all().values()
                dept_ids = [dept.get('id') for dept in list(dept)]
                ret += dept_ids
            return ret
        except:
            return []


@router.post("/role", response=SchemaOut)
def create_role(request, data: SchemaIn):
    dict_data = data.dict()
    del dict_data['menu']
    del dict_data['permission']
    del dict_data['dept']
    del dict_data['column']
    del dict_data['user']

    role = create(request, dict_data, Role)
    return role


@router.delete("/role/{role_id}")
def delete_role(request, role_id: int):
    delete(role_id, Role)
    return {"success": True}


@router.put("/role/{role_id}", response=SchemaOut)
def update_role(request, role_id: int, payload: SchemaIn):
    post = get_object_or_404(Role, id=role_id)
    for attr, value in payload.dict().items():
        if attr == 'menu':
            post.menu.set(value)
        elif attr == 'permission':
            post.permission.set(value)
        elif attr == 'dept':  # 背后这个字段目前不用，但必须留着
            post.dept.set(value)
        elif attr == 'column':
            post.column.set(value)
        elif attr == 'user':
            # 处理用户
            user_ids = [user_id-1000000 for user_id in value if user_id>1000000]
            users_to_associate = Users.objects.filter(id__in=user_ids)
            for user in users_to_associate:
                user.role.add(post)
            other_users = Users.objects.exclude(id__in=user_ids)
            for user in other_users:
                user.role.remove(post)
            
            # 处理部门
            dept_ids = [dept_id for dept_id in value if dept_id<1000000]
            post.dept.set(dept_ids)
        else:
            setattr(post, attr, value)
    post.save()
    return post


@router.get("/role", response=List[SchemaOut])
@paginate(MyPagination)
def list_role(request, filters: Filters = Query(...)):
    qs = retrieve(request, Role, filters)
    return qs


@router.get("/role/all/list", response=List[SchemaOut])
def all_list_role(request):
    qs = retrieve(request, Role)
    return qs


@router.get("/role/{role_id}", response=SchemaOut)
def get_role(request, role_id: int):
    role = get_object_or_404(Role, id=role_id)
    return role


class ButtonColumnFilters(FuFilters):
    menu_ids: list = Field(None, alias="menu_ids")


@router.get("/role/list/menu_button")
def list_menu_button_tree(request, filters: ButtonColumnFilters = Query(...)):
    qs = Menu.objects.filter()
    result = []
    menu_button_list = []

    for item in qs:
        dict_item = item.__dict__
        menu_button = list(item.menuPermission.all().values())

        for button_item in menu_button:
            button_item['id'] = f"b{button_item['id']}"
            button_item['parent_id'] = button_item.pop('menu_id')
            button_item['title'] = button_item.pop('name')

        # dict_item['menu_button'] = list(item.menuPermission.all().values())
        del dict_item['_state']
        result.extend(menu_button)
        result.append(dict_item)
    return get_button_or_column_menu(result, 'b')


@router.get("/role/list/menu_column")
def list_menu_column_tree(request, filters: ButtonColumnFilters = Query(...)):
    qs = Menu.objects.all()
    result = []
    for item in qs:
        dict_item = item.__dict__
        column_field = list(item.menuColumnField.all().values())
        for column_field_item in column_field:
            column_field_item['id'] = f"c{column_field_item['id']}"
            column_field_item['parent_id'] = column_field_item.pop('menu_id')
            column_field_item['title'] = column_field_item.pop('name')

        del dict_item['_state']
        result.append(dict_item)
        result.extend(column_field)

    return get_button_or_column_menu(result, 'c')


class SchemaMenuOut(ModelSchema):
    class Config:
        model = Menu
        model_fields = "__all__"


@router.get("/role/list/menu", response=List[SchemaMenuOut])
def list_menu_tree(request, filters: Filters = Query(...)):
    qs = retrieve(request, Menu, filters).values()
    # 将查询集转换成树形结构
    menu_tree = list_to_tree(list(qs))
    return FuResponse(data=menu_tree)

class SchemaUserOut(ModelSchema):
    class Config:
        model = Dept
        model_fields = "__all__"

@router.get("/role/list/user", response=List[SchemaUserOut])
def list_user_tree(request, filters: Filters = Query(...)):
    qs = retrieve(request, Dept, filters).values()
    # 将查询集转换成树形结构
    users = retrieve(request, Users, filters).values()
    # TODO 注意这里有特殊处理：用户id要加一百万，部门id不用
    users = [{**user, 'user_id':user.get('id'), 'id': 1000000+user.get('id'), 'parent_id': user.get('dept_id')} for user in list(users)]
    user_tree = list_to_tree(list(qs)+ list(users))
    return FuResponse(data=user_tree)

# class SchemaButtonOut(ModelSchema):
#     class Config:
#         model = MenuButton
#         model_fields = "__all__"
#
#
# @router.get("/role/list/button/{menu_id}", response=List[SchemaButtonOut])
# def get_button_by_menu_id(request, menu_id: int):
#     filters: Filters
#     qs = MenuButton.objects.filter(menu_id=menu_id)
#
#     return qs


def get_button_or_column_menu(data, flag):
    return_data = []
    for i in data:
        m_id = i['id']
        if flag in str(m_id):
            return_data.append(i)
            get_menu_by_parent(i['parent_id'], data, return_data)
    return return_data


def get_menu_by_parent(parent_id, data, return_data):
    for i in data:
        if parent_id == i['id'] and i not in return_data:
            return_data.append(i)
            get_menu_by_parent(i['parent_id'], data, return_data)
    if parent_id is None:
        return

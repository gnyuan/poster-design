# -*- coding: utf-8 -*-
# @Time    : 2022/6/2 23:19
# @Author  : 臧成龙
# @FileName: fu_auth.py
# @Software: PyCharm
# -*- coding: utf-8 -*-

import re
from datetime import datetime
import logging

# from django.core.cache import cache
from django.db.models import Q, F
from fuadmin.settings import DEMO, SECRET_KEY, WHITE_LIST
from ninja.security import HttpBearer
from system.models import MenuButton, Users, ApiWhiteList, Role

from .fu_jwt import FuJwt
from .fu_ninja import FuFilters
from .usual import get_dept, get_user_info_from_token
logger = logging.getLogger(__name__)

METHOD = {
    'GET': 0,
    'POST': 1,
    'PUT': 2,
    'DELETE': 3,
}


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt = FuJwt(SECRET_KEY)
        value = jwt.decode(SECRET_KEY, token)
        time_now = int(datetime.now().timestamp())
        # 判断token是否过期
        if value.valid_to >= time_now:
            token_user = value.payload
            token_user_id = token_user['id']
            user = Users.objects.get(id=token_user_id)
            request_path = request.path
            request_method = request.method

            # ***接口白名单***
            api_white_list = ApiWhiteList.objects.filter(enable_datasource=False).values(
                permission__api=F("url"), permission__method=F("method")
            )
            api_white_list = [
                str(item.get("permission__api").replace("{id}", ".*?")) + ":" + str(item.get("permission__method"))
                for item in api_white_list
                if item.get("permission__api")
            ]
            for item in api_white_list:
                new_api = request_path + f":{METHOD[request_method]}" 
                matchObj = re.match(item, new_api, re.M | re.I)
                if matchObj is None:
                    continue
                else:
                    logger.info(f'hit apiwhitelist item={item}, new_api={new_api}')
                    return token
            if DEMO:
                # 判断是否在白名单中
                if request_path in WHITE_LIST:
                    return token
                if request_method == 'GET':
                    return token
                else:
                    logger.info(f'in Demo mode, no permission, user={user.username}, request_path={request_path}, request_method={request_method}')
                    raise TimeoutError(403, '演示环境')
            else:
                # 判断是否是超级管理员
                if not token_user['is_superuser']:
                    # 判断是path是否是‘/数字’结尾
                    result = re.search(r'/\d+$', request_path)
                    if result:
                        match_value = result.group()
                        # 将数字结尾的接口替换成.*? 因为接口中是/{id}
                        request_path = request_path.replace(match_value, '/*')
                    # 判断是否在白名单中
                    if request_path in WHITE_LIST:
                        return token
                    else:
                        menuButtonIds = user.role.values_list('permission__id', flat=True)
                        # 该用户所属部门，如果给部门赋予了角色，则也有可能有菜单按钮权限
                        user_departments = [user.dept]
                        def get_sub_departments(department):
                            sub_departments = department.dept_set.all()
                            for sub_dept in sub_departments:
                                user_departments.append(sub_dept)
                                get_sub_departments(sub_dept)

                        get_sub_departments(user.dept)
                        other_menuButtonIds = Role.objects.filter(dept__in=user_departments).values_list('permission__id', flat=True)

                        queryset = MenuButton.objects.filter(id__in=menuButtonIds.union(other_menuButtonIds), api__regex=request_path,
                                                             method=METHOD[request_method])
                        if queryset.exists():
                            return token
                        else:
                            logger.info(f'no permission, user={user.username}, request_path={request_path}, request_method={request_method}')
                            raise TimeoutError(403, '没有权限')
            # cache_token = cache.get(token_user_id)
            # if token == cache_token:
            return token
        else:
            raise TimeoutError(401, 'token时间过期')


def data_permission(request, filters: FuFilters):
    user_info = get_user_info_from_token(request)
    if user_info['is_superuser']:
        return filters
    user = Users.objects.get(id=user_info['id'])
    data_range_qs = user.role.values_list('data_range', flat=True)

    # 该用户所属部门，如果给部门赋予了角色，则也有可能有菜单
    user_departments = [user.dept]
    def get_sub_departments(department):
        sub_departments = department.dept_set.all()
        for sub_dept in sub_departments:
            user_departments.append(sub_dept)
            get_sub_departments(sub_dept)

    get_sub_departments(user.dept)
    other_data_range_qs = Role.objects.filter(dept__in=user_departments).values_list('data_range', flat=True)

    # 如果有多个角色，取数据权限最大的角色
    data_range = max(list(data_range_qs) + list(other_data_range_qs))

    # 仅本人数据权限
    if data_range == 0:
        filters.creator_id = user_info['id']

    # 本部门数据权限
    if data_range == 1:
        filters.belong_dept = user_info['dept']

    # 本部门及以下数据权限
    if data_range == 2:
        dept_and_below_ids = get_dept(user_info['dept'])
        filters.belong_dept__in = dept_and_below_ids

    # 自定义数据权限
    if data_range == 3:
        dept_ids = user.role.values_list('dept__id', flat=True)
        filters.belong_dept__in = list(dept_ids)

    # 所有数据权限
    if data_range == 4:
        pass

    return filters




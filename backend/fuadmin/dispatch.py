#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q

dispatch_db_type = getattr(settings, 'DISPATCH_DB_TYPE', 'memory')  # redis


# ================================================= #
# ******************** 初始化 ******************** #
# ====================================-============= #

def _get_all_system_config():
    data = {}
    from system.models import SystemConfig

    system_config_obj = (
        SystemConfig.objects.filter(~Q(parent_id__form_item_type=11), parent_id__isnull=False)
        .values("parent__key", "key", "value", "form_item_type")
        .order_by("sort")
    )
    for system_config in system_config_obj:
        value = system_config.get("value", "")
        if value and system_config.get("form_item_type") == 7:
            value = value[0].get("url")
        if value and system_config.get("form_item_type") == 11:
            new_value = []
            for ele in value:
                new_value.append({
                    "key": ele.get('key'),
                    "title": ele.get('title'),
                    "value": ele.get('value'),
                })
            new_value.sort(key=lambda s: s["key"])
            value = new_value
        data[f"{system_config.get('parent__key')}.{system_config.get('key')}"] = value
    return data

def init_system_config():
    """
    初始化系统配置
    :param name:
    :return:
    """
    try:
        if dispatch_db_type == 'redis':
            cache.set(f"init_system_config", _get_all_system_config())
            return
        settings.SYSTEM_CONFIG = _get_all_system_config()
    except Exception as e:
        print("请先进行数据库迁移!")
    return


def refresh_system_config():
    """
    刷新系统配置
    :return:
    """
    if dispatch_db_type == 'redis':
        cache.set(f"init_system_config", _get_all_system_config())
        return
    settings.SYSTEM_CONFIG = _get_all_system_config()


# ================================================= #
# ******************** 系统配置 ******************** #
# ================================================= #
def get_system_config(schema_name=None):
    """
    获取系统配置中所有配置
    1.只传父级的key，返回全部子级，{ "父级key.子级key" : "值" }
    2."父级key.子级key"，返回子级值
    :param schema_name: 对应字典配置的租户schema_name值
    :return:
    """
    if dispatch_db_type == 'redis':
        init_dictionary_data = cache.get(f"init_system_config")
        if not init_dictionary_data:
            refresh_system_config()
        return cache.get(f"init_system_config") or {}
    if not settings.SYSTEM_CONFIG:
        refresh_system_config()
    dictionary_config = settings.SYSTEM_CONFIG
    return dictionary_config or {}


def get_system_config_values(key, schema_name=None):
    """
    获取系统配置数据数组
    :param key: 对应系统配置的key值(字典编号)
    :param schema_name: 对应系统配置的租户schema_name值
    :return:
    """
    if dispatch_db_type == 'redis':
        system_config = cache.get(f"init_system_config")
        if not system_config:
            refresh_system_config()
            system_config = cache.get(f"init_system_config")
        return system_config.get(key)
    system_config = get_system_config(schema_name)
    return system_config.get(key)


def get_system_config_values_to_dict(key, schema_name=None):
    """
    获取系统配置数据并转换为字典 **仅限于数组类型系统配置
    :param key: 对应系统配置的key值(字典编号)
    :param schema_name: 对应系统配置的租户schema_name值
    :return:
    """
    values_dict = {}
    config_values = get_system_config_values(key, schema_name)
    if not isinstance(config_values, list):
        raise ValueError("该方式仅限于数组类型系统配置")
    for ele in get_system_config_values(key, schema_name):
        values_dict[ele.get('key')] = ele.get('value')
    return values_dict


def get_system_config_label(key, name, schema_name=None):
    """
    获取获取系统配置label值
    :param key: 系统配置中的key值(字典编号)
    :param name: 对应系统配置的value值
    :param schema_name: 对应系统配置的租户schema_name值
    :return:
    """
    children = get_system_config_values(key, schema_name) or []
    for ele in children:
        if ele.get("value") == str(name):
            return ele.get("label")
    return ""

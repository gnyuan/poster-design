# 城市联动
"""
到乡级 使用方法
1. https://www.npmjs.com/package/china-division 下载数据，把对应的json放入对应目录
2. 修改此文件中对应json名
3. 右击执行此py文件进行初始化
"""
import json
import os

import django
import pypinyin
from django.core.management import BaseCommand
from django.db import connection

from fuadmin.settings import BASE_DIR
from system.models import Area

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()


def area_list(code_list, parent_id=None, depth=1):
    """
    递归获取所有列表
    """
    for i, code_dict in enumerate(code_list):
        code = code_dict.get('code', None)
        name = code_dict.get('name', None)
        children = code_dict.get('children', None)
        pinyin = ''.join([''.join(i) for i in pypinyin.pinyin(name, style=pypinyin.NORMAL)])
        area: Area = Area.objects.create( **{
                "name": name,
                "code": code,
                "level": depth,
                "pinyin": pinyin,
                "initials": pinyin[0].upper() if pinyin else "#",
                "parent_id": parent_id,
                "creator_id": 1,
                'sort': i+1,
            })
        if children:
            area_list(code_list=children, parent_id=area.id, depth=depth + 1)


def main():
    with open(os.path.join(BASE_DIR, 'system', 'management', 'commands','pca-code.json'), 'r',encoding="utf-8") as load_f:
        code_list = json.load(load_f)
    
    if Area.objects.count() == 0:
        area_list(code_list)
    else:
        print('省份数据已经存在，无需初始化')


class Command(BaseCommand):
    """
    项目初始化命令: python manage.py init
    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        print(f"正在准备初始化省份数据...")

        if hasattr(connection, 'tenant') and connection.tenant.schema_name:
            from django_tenants.utils import get_tenant_model
            from django_tenants.utils import tenant_context,schema_context
            for tenant in get_tenant_model().objects.exclude(schema_name='public'):
                with tenant_context(tenant):
                    print(f"租户[{connection.tenant.schema_name}]初始化数据开始...")
                    main()
                    print(f"租户[{connection.tenant.schema_name}]初始化数据完成！")
        else:
            main()
        print("省份数据初始化数据完成！")


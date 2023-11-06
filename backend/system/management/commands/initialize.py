# 初始化
import datetime
import os
import django
import json

from fuadmin.settings import BASE_DIR
from system.models import Dept, Menu, MenuButton, Role, Post, Users, Dict, DictItem, CategoryDict, ApiWhiteList, SystemConfig
from design.models import Templ, Cate, Font
from utils.core_initialize import CoreInitialize
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

class Initialize(CoreInitialize):
    creator_id = 1

    def init_dept(self):  # 初始化部门信息
        def dept_list(code_list, parent_id=None):
            for i, code_dict in enumerate(code_list):
                dept: Dept = Dept.objects.create(**{
                    "name": code_dict.get('name', None),
                    "phone": code_dict.get('phone', None),
                    "email": code_dict.get('email', None),
                    "modifier": code_dict.get('modifier', None),
                    "belong_dept": code_dict.get('belong_dept', None),
                    "update_datetime": datetime.datetime.now(),
                    "update_datetime": datetime.datetime.now(),
                    "parent_id": parent_id,
                    "creator_id": 1,
                    'sort': i+1,
                })
                if code_dict.get('children', None):
                    dept_list(code_list=code_dict.get(
                        'children', None), parent_id=dept.id)

        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_dept.json'), 'r', encoding="utf-8") as load_f:
            code_list = json.load(load_f)

            if Dept.objects.count() == 0:
                dept_list(code_list)
            else:
                print('dept数据已经存在，无需初始化')

    def init_users(self):
        """
        初始化用户表
        """
        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_user.json'), 'r', encoding="utf-8") as load_f:
            user_list = json.load(load_f)
            if Users.objects.count() == 0:
                for user in user_list:
                    Users.objects.create(**{
                        "password": user.get('password', None),
                        "is_superuser": user.get('is_superuser', None),
                        "first_name": user.get('first_name', None),
                        "last_name": user.get('last_name', None),
                        "is_staff": user.get('is_staff', None),
                        "is_active": user.get('is_active', None),
                        "username": user.get('username', None),
                        "email": user.get('email', None),
                        "mobile": user.get('mobile', None),
                        "name": user.get('name', None),
                        "gender": user.get('gender', None),
                        "user_type": user.get('user_type', None),
                        "status": user.get('status', None),
                        "avatar": user.get('avatar', None),
                        "remark": user.get('remark', None),
                        "creator_id": 1,
                        "belong_dept": user.get('belong_dept', None),
                        "modifier": user.get('modifier', None),
                        "update_datetime": datetime.datetime.now(),
                        "update_datetime": datetime.datetime.now(),
                    })
            else:
                print('Users数据已经存在，无需初始化')

    def init_menu(self):  # 初始化菜单信息
        def menu_list(code_list, parent_id=None):
            """
            递归获取所有列表
            """
            for i, code_dict in enumerate(code_list):
                menu: Menu = Menu.objects.create(**{
                    "modifier": code_dict.get('modifier', None),
                    "belong_dept": code_dict.get('belong_dept', None),
                    "icon": code_dict.get('icon', None),
                    "title": code_dict.get('title', None),
                    "permission": code_dict.get('permission', None),
                    "is_ext": code_dict.get('is_ext', None),
                    "from_src": code_dict.get('from_src', None),
                    "type": code_dict.get('type', None),
                    "path": code_dict.get('path', None),
                    "redirect": code_dict.get('redirect', None),
                    "component": code_dict.get('component', None),
                    "name": code_dict.get('name', None),
                    "status": code_dict.get('status', None),
                    "keepalive": code_dict.get('keepalive', None),
                    "hide_menu": code_dict.get('hide_menu', None),
                    "update_datetime": datetime.datetime.now(),
                    "update_datetime": datetime.datetime.now(),
                    "parent_id": parent_id,
                    "creator_id": 1,
                    'sort': i+1,
                })
                if code_dict.get('auth'):  # 如果该菜单有配置按钮权限
                    auth_list = code_dict.get('auth')
                    for auth in auth_list:
                        MenuButton.objects.create(**{
                            "name": auth.get('name', None),
                            "code": auth.get('code', None),
                            "api": auth.get('api', None),
                            "method": auth.get('method', None),
                            "creator_id": 1,
                            "belong_dept": code_dict.get('belong_dept', None),
                            "modifier": code_dict.get('modifier', None),
                            "update_datetime": datetime.datetime.now(),
                            "update_datetime": datetime.datetime.now(),
                            "menu_id": menu.id,
                        })
                if code_dict.get('children', None):
                    menu_list(code_list=code_dict.get(
                        'children', None), parent_id=menu.id)

        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_menu.json'), 'r', encoding="utf-8") as load_f:
            code_list = json.load(load_f)

            if Menu.objects.count() == 0:
                menu_list(code_list)
            else:
                print('菜单数据已经存在，无需初始化')

    def init_dictcategory(self):
        def categorydict_list(code_list, parent_id=None):
            """
            递归获取所有categorydict_list
            """
            for i, code_dict in enumerate(code_list):
                category: CategoryDict = CategoryDict.objects.create(**{
                    "modifier": code_dict.get('modifier', None),
                    "belong_dept": code_dict.get('belong_dept', None),
                    "update_datetime": datetime.datetime.now(),
                    "update_datetime": datetime.datetime.now(),
                    "sort": i+1,
                    "parent_id": parent_id,
                    "creator_id": 1,
                    "label": code_dict.get('label', None),
                    "value": code_dict.get('value', None),
                    "code": code_dict.get('code', None),
                    
                })
                
                if code_dict.get('children', None):
                    categorydict_list(code_list=code_dict.get(
                        'children', None), parent_id=category.id)

        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_dictcategory.json'), 'r', encoding="utf-8") as load_f:
            dictcategory = json.load(load_f)

            if CategoryDict.objects.count() == 0:
                categorydict_list(dictcategory)
            else:
                print('DictCattegory数据已经存在，无需初始化')


    def init_role(self):  # 初始化角色表

        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_role.json'), 'r', encoding="utf-8") as load_f:
            role_list = json.load(load_f)

            if Role.objects.count() == 0:
                for role in role_list:
                    Role.objects.create(**{
                        "name": role.get('name', None),
                        "code": role.get('code', None),
                        "status": role.get('status', None),
                        "admin": role.get('admin', None),
                        "data_range": role.get('data_range', None),
                        "remark": role.get('remark', None),
                        "creator_id": 1,
                        "belong_dept": role.get('belong_dept', None),
                        "modifier": role.get('modifier', None),
                        "update_datetime": datetime.datetime.now(),
                        "update_datetime": datetime.datetime.now(),
                    })
            else:
                print('角色数据已经存在，无需初始化')

    def init_apiwhitelist(self):  # 初始化接口白名单

        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_apiwhitelist.json'), 'r', encoding="utf-8") as load_f:
            api_list = json.load(load_f)

            if ApiWhiteList.objects.count() == 0:
                for api in api_list:
                    ApiWhiteList.objects.create(**{
                        "url": api.get('url', None),
                        "method": api.get('method', None),
                        "enable_datasource": api.get('enable_datasource', False),
                        "remark": api.get('remark', None),
                        "creator_id": 1,
                        "belong_dept": api.get('belong_dept', None),
                        "modifier": api.get('modifier', None),
                        "update_datetime": datetime.datetime.now(),
                        "update_datetime": datetime.datetime.now(),
                    })
            else:
                print('接口白名单数据已经存在，无需初始化')

    def init_dict(self): # 初始化字典及对应的字典值 Dict DictItem
        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_dict.json'), 'r', encoding="utf-8") as load_f:
            dictionary_list = json.load(load_f)

            if Dict.objects.count() == 0:
                for i, dictionary in enumerate(dictionary_list):
                    mydictionary = Dict.objects.create(**{
                        "modifier": dictionary.get('modifier', '超级管理员'),
                        "belong_dept": dictionary.get('belong_dept', None),
                        "update_datetime": datetime.datetime.now(),
                        "create_datetime": datetime.datetime.now(),
                        "sort": dictionary.get('sort', i+1),
                        "name": dictionary.get('name', None),
                        "code": dictionary.get('code', None),
                        "status": dictionary.get('status', 1),
                        "remark": dictionary.get('remark', None),
                        "creator_id": 1,
                    })

                    for j, child in enumerate(dictionary.get('children', [])):
                        DictItem.objects.create(**{
                            "modifier": child.get('modifier', '超级管理员'),
                            "belong_dept": child.get('belong_dept', None),
                            "update_datetime": datetime.datetime.now(),
                            "create_datetime": datetime.datetime.now(),
                            "sort": child.get('sort', j+1),
                            "label": child.get('label', None),
                            "value": child.get('value', None),
                            "icon": child.get('icon', ""),
                            "status": child.get('status', 1),
                            "remark": child.get('remark', None),
                            "creator_id": 1,
                            "dict_id": mydictionary.id,
                        })
            else:
                print('字典数据已经存在，无需初始化')

    def init_task(self):
        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_task.json'), 'r', encoding="utf-8") as load_f:
            task_list = json.load(load_f)
            if IntervalSchedule.objects.count() == 0:
                for _, row in enumerate(task_list):
                    internal: IntervalSchedule = IntervalSchedule.objects.create(**{"every": row.get('every'),"period": row.get('period')})
                    if row.get('children'):
                        for task in row.get('children'):
                            task: PeriodicTask = PeriodicTask.objects.create(**{"name": task.get('name'),"task": task.get('task'), "interval_id": internal.id})
            else:
                print('定时任务数据已经存在，无需初始化')
    
    def init_systemconfig(self):
        def systemconfig_list(code_list, parent_id=None):
            """
            递归获取所有列表
            """
            for i, code_dict in enumerate(code_list):
                config: SystemConfig = SystemConfig.objects.create(**{
                    "title": code_dict.get('title', None),
                    "key": code_dict.get('key', None),
                    "status": code_dict.get('status', None),
                    "data_options": code_dict.get('data_options', None),
                    "form_item_type": code_dict.get('form_item_type', None),
                    "rule": code_dict.get('rule', None),
                    "placeholder": code_dict.get('placeholder', None),
                    "setting": code_dict.get('setting', None),
                    "modifier": code_dict.get('modifier', None),
                    "belong_dept": code_dict.get('belong_dept', None),
                    "update_datetime": datetime.datetime.now(),
                    "update_datetime": datetime.datetime.now(),
                    "parent_id": parent_id,
                    "creator_id": 1,
                    'sort': i+1,
                })
                if code_dict.get('children', None):
                    systemconfig_list(code_list=code_dict.get(
                        'children', None), parent_id=config.id)

        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_systemconfig.json'), 'r', encoding="utf-8") as load_f:
            code_list = json.load(load_f)

            if SystemConfig.objects.count() == 0:
                systemconfig_list(code_list)
            else:
                print('系统配置已经存在，无需初始化')

    def init_poster_template(self):  # 初始化poster
        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_poster_template.json'), 'r', encoding="utf-8") as load_f:
            api_list = json.load(load_f)

            if Templ.objects.count() == 0:
                for api in api_list:
                    Templ.objects.create(**{
                        'cover': api.get('cover', ''),
                        'url': api.get('url', ''),
                        'type': api.get('type', 0),
                        'title': api.get('title', ''),
                        'name': api.get('name', ''),
                        'search': api.get('search', ''),
                        'data': api.get('data', ''),
                        'content': api.get('content', ''),
                        'width': api.get('width', 0),
                        'height': api.get('height', 0),
                        'state': api.get('state', 1),
                        'cate_id': api.get('cate', 1),
                        'category': api.get('category', 0),
                        'resource': api.get('resource', ''),
                        'tag': api.get('tag', ''),

                        "remark": api.get('remark', None),
                        "creator_id": 1,
                        "belong_dept": api.get('belong_dept', None),
                        "modifier": api.get('modifier', None),
                        "update_datetime": datetime.datetime.now(),
                        "update_datetime": datetime.datetime.now(),
                    })
            else:
                print('poster_tempalte数据已经存在，无需初始化')
    def init_poster_cate(self):  # 初始化poster
        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_poster_cate.json'), 'r', encoding="utf-8") as load_f:
            api_list = json.load(load_f)

            if Cate.objects.count() == 0:
                for api in api_list:
                    Cate.objects.create(**{
                        'type': api.get('type', 0),
                        'name': api.get('name', ''),
                        "remark": api.get('remark', None),
                        "creator_id": 1,
                        "belong_dept": api.get('belong_dept', None),
                        "modifier": api.get('modifier', None),
                        "update_datetime": datetime.datetime.now(),
                        "update_datetime": datetime.datetime.now(),
                    })
            else:
                print('poster_tempalte数据已经存在，无需初始化')
    def init_poster_font(self):  # 初始化poster
        with open(os.path.join(BASE_DIR, 'system', 'management', 'commands', 'init_poster_font.json'), 'r', encoding="utf-8") as load_f:
            api_list = json.load(load_f)
            if Font.objects.count() == 0:
                for api in api_list:
                    Font.objects.create(**{
                        'oid': api.get('oid', 1),
                        'alias': api.get('alias', ''),
                        'preview': api.get('preview', ''),
                        'ttf': api.get('ttf', ''),
                        'woff': api.get('woff', ''),
                        'value': api.get('value', ''),
                        'font_family': api.get('font_family', ''),
                        'size': api.get('size', 0),
                        'version': api.get('version', ''),
                        'lang': api.get('lang', ''),
                        'woff_size': api.get('woff_size', 0),
                        "remark": api.get('remark', None),
                        "creator_id": 1,
                        "belong_dept": api.get('belong_dept', None),
                        "modifier": api.get('modifier', None),
                        "update_datetime": datetime.datetime.now(),
                        "update_datetime": datetime.datetime.now(),
                    })
            else:
                print('poster_tempalte数据已经存在，无需初始化')
    def run(self):
        self.init_dept()
        self.init_users()
        self.init_menu()
        self.init_dict()
        self.init_dictcategory()
        self.init_role()
        self.init_task()
        self.init_apiwhitelist()
        self.init_systemconfig()
        self.init_poster_cate()
        self.init_poster_template()
        self.init_poster_font()
        


# 项目init 初始化，默认会执行 main 方法进行初始化
def main(reset=False):
    Initialize(reset).run()
    pass


if __name__ == '__main__':
    main()

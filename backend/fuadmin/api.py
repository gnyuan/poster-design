# -*- coding: utf-8 -*-
# @Time    : 2022/5/9 23:15
# @Author  : 臧成龙
# @FileName: api.py
# @Software: PyCharm
from system.router import system_router
from design.router import design_router
from utils.fu_auth import GlobalAuth
from utils.fu_ninja import FuNinjaAPI
import logging
import traceback

api = FuNinjaAPI(auth=GlobalAuth(), title="XunPai API")
logger = logging.getLogger(__file__)


# 统一处理server异常
@api.exception_handler(Exception)
def a(request, exc):
    logger.error(str(exc) + str(traceback.format_exc()))
    if hasattr(exc, 'errno'):
        return api.create_response(request, data=[], msg=str(exc) + str(traceback.format_exc()), code=exc.errno)
    else:
        return api.create_response(request, data=[], msg=str(exc) + str(traceback.format_exc()), code=500)


api.add_router('/system/', system_router)
api.add_router('/design/', design_router)

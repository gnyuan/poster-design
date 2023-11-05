from ninja import Router, Schema, Query, Field, ModelSchema
from ninja.pagination import paginate
from django.shortcuts import get_object_or_404
from system.models import SystemConfig
from utils.fu_crud import create, delete, retrieve
from utils.fu_ninja import FuFilters
from utils.fu_ninja import MyPagination
from utils.fu_response import FuResponse
from typing import List
from fuadmin import dispatch, websocketConfig

router = Router()


class Filters(FuFilters):
    key: str = Field(None, alias="key")
    status: bool = Field(None, alias="status")
    id: str = Field(None, alias="id")


class SchemaIn(ModelSchema):
    class Config:
        model = SystemConfig
        model_exclude = ['id', 'create_datetime', 'update_datetime']



class SchemaOut(ModelSchema):
    class Config:
        model = SystemConfig
        model_fields = "__all__"


@router.post("/system_config", response=SchemaOut)
def create_system_config(request, data: SchemaIn):
    dict_data = data.dict()
    system_config = create(request, dict_data, SystemConfig)
    dispatch.refresh_system_config()  # 有更新则刷新系统配置
    # websocketConfig.websocket_push("user_512", message={"sender": 'system', "contentType": 'SYSTEM',
    #                                        "content": '系统配置有变化~', "systemConfig": True})
    return system_config


@router.delete("/system_config/{system_config_id}")
def delete_system_config(request, system_config_id: int):
    delete(system_config_id, SystemConfig)
    dispatch.refresh_system_config()  # 有更新则刷新系统配置
    return {"success": True}


@router.put("/system_config/{system_config_id}", response=SchemaOut)
def update_system_config(request, system_config_id: int, payload: SchemaIn):
    post = get_object_or_404(SystemConfig, id=system_config_id)
    post.save()
    dispatch.refresh_system_config()  # 有更新则刷新系统配置
    return post


@router.get("/system_config", response=List[SchemaOut])
@paginate(MyPagination)
def list_system_config(request, filters: Filters = Query(...)):
    qs = retrieve(request, SystemConfig, filters)
    return qs


@router.get("/system_config/all/list", response=List[SchemaOut])
def all_list_system_config(request):
    qs = retrieve(request, SystemConfig)
    from fuadmin import websocketConfig
    # websocketConfig.websocket_push("user_512", message={"sender": 'system', "contentType": 'SYSTEM',
    #                                        "content": '服务端发给user512的', "systemConfig": True})
    return qs


from typing import List

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router
from ninja.pagination import paginate
from system.models import ApiWhiteList
from utils.fu_crud import (
    create,
    delete,
    retrieve,
    update,
)
from utils.fu_ninja import FuFilters, MyPagination

router = Router()


class Filters(FuFilters):
    url: str = Field(None, alias="url")
    method: str = Field(None, alias="method")
    enable_datasource: int = Field(None, alias="enable_datasource")
    remark: str = Field(None, alias="remark")

    id: str = Field(None, alias="apiwhitelist_id")


class WhitelistSchemaIn(ModelSchema):
    class Config:
        model = ApiWhiteList
        model_fields = ['url', 'method', 'enable_datasource', 'remark']


class WhitelistSchemaOut(ModelSchema):
    class Config:
        model = ApiWhiteList
        model_fields = "__all__"


@router.post("/whitelist", response=WhitelistSchemaOut)
def create_post(request, data: WhitelistSchemaIn):
    post = create(request, data, ApiWhiteList)
    return post


@router.delete("/whitelist/{whitelist_id}")
def delete_post(request, whitelist_id: int):
    delete(whitelist_id, ApiWhiteList)
    return {"success": True}


@router.put("/whitelist/{whitelist_id}", response=WhitelistSchemaOut)
def update_post(request, whitelist_id: int, data: WhitelistSchemaIn):
    post = update(request, whitelist_id, data, ApiWhiteList)
    return post


@router.get("/whitelist", response=List[WhitelistSchemaOut])
@paginate(MyPagination)
def list_post(request, filters: Filters = Query(...)):
    qs = retrieve(request, ApiWhiteList, filters)
    return qs


@router.get("/whitelist/{whitelist_id}", response=WhitelistSchemaOut)
def get_post(request, whitelist_id: int):
    whitelist = get_object_or_404(ApiWhiteList, id=whitelist_id)
    return whitelist


@router.get("/whitelist/all/list", response=List[WhitelistSchemaOut])
def all_list_post(request):
    qs = retrieve(request, ApiWhiteList)
    return qs

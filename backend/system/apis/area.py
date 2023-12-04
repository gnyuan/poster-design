from typing import List

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from system.models import Area, Dept
from utils.fu_crud import create, delete, retrieve, update
from utils.fu_ninja import FuFilters, MyPagination
from utils.fu_response import FuResponse
from utils.list_to_tree import aync_list_to_tree

router = Router()

class Filters(FuFilters):
    name: str = Field(None, alias="name")
    status: bool = Field(None, alias="status")
    code: str = Field(None, alias="code")
    id: str = Field(None, alias="id")
    level: int = Field(None, alias="level")
    parent_id: str = Field(None, alias="parent_id")


class SchemaIn(ModelSchema):

    class Config:
        model = Area
        model_exclude = ['id', 'create_datetime', 'update_datetime']


class SchemaOut(ModelSchema):

    class Config:
        model = Area
        model_fields = "__all__"
    # model_fields = []


@router.post("/area", response=SchemaOut)
def create_area(request, data: SchemaIn):
    area = create(request, data, Area)
    return area


@router.delete("/area/{area_id}")
def delete_area(request, area_id: int):
    delete(area_id, Area)
    return {"success": True}


@router.put("/area/{area_id}", response=SchemaOut)
def update_area(request, area_id: int, data: SchemaIn):
    area = update(request, area_id, data, Area)
    return area


@router.get("/area", response=List[SchemaOut])
@paginate(MyPagination)
def list_area(request, filters: Filters = Query(...)):
    qs = retrieve(request, Area, filters)
    return qs


@router.get("/area/{area_id}", response=SchemaOut)
def get_area(request, area_id: int):
    area = get_object_or_404(Area, id=area_id)
    return area

# 懒加载树只有两个参数有用，id和level
@router.get("/area/list/tree")
def list_area_tree(request, filters: Filters = Query(...)):
    qs = retrieve(request, Area).values()
    if filters.parent_id:
        area_tree = aync_list_to_tree(list(qs), parent_id=filters.parent_id)
    else:
        area_tree = aync_list_to_tree(list(qs), deepLimit=filters.level)
    return FuResponse(data=area_tree)


# 通过name或者code进行搜索
@router.get("/area/list/search", response=List[SchemaOut])
def list_area_tree(request, filters: Filters = Query(...)):
    ret = retrieve(request, Area).values()
    if not filters.name and not filters.code:
        # 直接返回上面那个接口的数据
        area_tree = aync_list_to_tree(list(ret), deepLimit=1)
        return FuResponse(data=area_tree)
    if filters.name:
        ret = ret.filter(name__contains=filters.name)
    if filters.code:
        ret = ret.filter(code__startswith=filters.code)
    
    return ret
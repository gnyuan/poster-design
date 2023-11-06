from typing import List

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from design.models import Cate
from utils.fu_crud import create, delete, retrieve, update
from utils.fu_ninja import FuFilters, MyPagination
from utils.fu_response import FuResponse

router = Router()


class Filters(FuFilters):
    name: str = Field(None, alias="name")
    type: int = Field(None, alias="type")
    id: str = Field(None, alias="id")


class SchemaIn(ModelSchema):
    parent_id: int = None

    class Config:
        model = Cate
        model_exclude = ['id', 'create_datetime', 'update_datetime']


class SchemaOut(ModelSchema):
    class Config:
        model = Cate
        model_fields = "__all__"
    # model_fields = []


@router.post("/cate", response=SchemaOut, auth=None)
def create_poster_template(request, data: SchemaIn):
    poster = create(request, data, Cate)
    return poster


@router.delete("/cate/{dept_id}", auth=None)
def delete_poster_template(request, dept_id: int):
    delete(dept_id, Cate)
    return {"success": True}


@router.put("/cate/{dept_id}", response=SchemaOut, auth=None)
def update_poster_template(request, dept_id: int, data: SchemaIn):
    poster = update(request, dept_id, data, Cate)
    return poster


@router.get("/cate", response=List[SchemaOut], auth=None)
@router.get("/list", response=List[SchemaOut], auth=None)
# @paginate(MyPagination)
def list_poster_template(request, filters: Filters = Query(...)):
    print(1111)
    print(filters)
    qs = retrieve(request, Cate, filters)
    return qs


@router.get("/cate/{dept_id}", response=SchemaOut, auth=None)
def get_poster_template(request, dept_id: int):
    poster = get_object_or_404(Cate, id=dept_id)
    return poster


from typing import List

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from design.models import Material
from utils.fu_crud import create, delete, retrieve, update
from utils.fu_ninja import FuFilters, MyPagination
from utils.fu_response import FuResponse

router = Router()


class Filters(FuFilters):
    name: str = Field(None, alias="name")
    type: int = Field(None, alias="type")
    id: str = Field(None, alias="id")
    category: int = Field(None, alias="cate")


class SchemaIn(ModelSchema):
    parent_id: int = None

    class Config:
        model = Material
        model_exclude = ['id', 'create_datetime', 'update_datetime']


class SchemaOut(ModelSchema):
    class Config:
        model = Material
        model_fields = "__all__"
    # model_fields = []


@router.post("/material", response=SchemaOut, auth=None)
def create_poster_template(request, data: SchemaIn):
    poster = create(request, data, Material)
    return poster


@router.delete("/material/{dept_id}", auth=None)
def delete_poster_template(request, dept_id: int):
    delete(dept_id, Material)
    return {"success": True}


@router.put("/material/{dept_id}", response=SchemaOut, auth=None)
def update_poster_template(request, dept_id: int, data: SchemaIn):
    poster = update(request, dept_id, data, Material)
    return poster


@router.get("/material", response=List[SchemaOut], auth=None)
@paginate(MyPagination)
def list_poster_template(request, filters: Filters = Query(...)):
    qs = retrieve(request, Material, filters)
    return qs


@router.get("/material/{dept_id}", response=SchemaOut, auth=None)
def get_poster_template(request, dept_id: int):
    poster = get_object_or_404(Material, id=dept_id)
    return poster


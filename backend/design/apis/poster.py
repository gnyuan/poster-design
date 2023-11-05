from typing import List

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from design.models import Templ
from utils.fu_crud import create, delete, retrieve, update
from utils.fu_ninja import FuFilters, MyPagination
from utils.fu_response import FuResponse

router = Router()


class Filters(FuFilters):
    name: str = Field(None, alias="name")
    status: bool = Field(None, alias="status")
    id: str = Field(None, alias="id")


class SchemaIn(ModelSchema):
    parent_id: int = None

    class Config:
        model = Templ
        model_exclude = ['id', 'create_datetime', 'update_datetime']


class SchemaOut(ModelSchema):
    class Config:
        model = Templ
        model_fields = "__all__"
    # model_fields = []


@router.post("/poster", response=SchemaOut)
def create_poster_template(request, data: SchemaIn):
    poster = create(request, data, Templ)
    return poster


@router.delete("/poster/{dept_id}")
def delete_poster_template(request, dept_id: int):
    delete(dept_id, Templ)
    return {"success": True}


@router.put("/poster/{dept_id}", response=SchemaOut)
def update_poster_template(request, dept_id: int, data: SchemaIn):
    poster = update(request, dept_id, data, Templ)
    return poster

@router.get('/design2/c3te', response=List[SchemaOut])
@router.get("/poster", response=List[SchemaOut])
@paginate(MyPagination)
def list_poster_template(request, filters: Filters = Query(...)):
    qs = retrieve(request, Templ, filters)
    return qs


@router.get("/poster/{dept_id}", response=SchemaOut)
def get_poster_template(request, dept_id: int):
    poster = get_object_or_404(Templ, id=dept_id)
    return poster


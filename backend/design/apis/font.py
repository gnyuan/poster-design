from typing import List

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from design.models import Font
from utils.fu_crud import create, delete, retrieve, update
from utils.fu_ninja import FuFilters, MyPagination
from utils.fu_response import FuResponse
import requests
import base64

router = Router()


class Filters(FuFilters):
    name: str = Field(None, alias="name")
    type: int = Field(None, alias="type")
    id: str = Field(None, alias="id")
    content: str = Field(None, alias="content")


class SchemaIn(ModelSchema):
    parent_id: int = None

    class Config:
        model = Font
        model_exclude = ['id', 'create_datetime', 'update_datetime']


class SchemaOut(ModelSchema):
    class Config:
        model = Font
        model_fields = "__all__"
    # model_fields = []


@router.post("/font", response=SchemaOut, auth=None)
def create_poster_template(request, data: SchemaIn):
    poster = create(request, data, Font)
    return poster


@router.delete("/font/{dept_id}", auth=None)
def delete_poster_template(request, dept_id: int):
    delete(dept_id, Font)
    return {"success": True}


@router.put("/font/{dept_id}", response=SchemaOut, auth=None)
def update_poster_template(request, dept_id: int, data: SchemaIn):
    poster = update(request, dept_id, data, Font)
    return poster


@router.get("/font", response=List[SchemaOut], auth=None)
@router.get("/fonts", response=List[SchemaOut], auth=None)
@paginate(MyPagination)
def list_poster_template(request, filters: Filters = Query(...)):
    qs = retrieve(request, Font, filters)
    return qs


@router.get("/font/{dept_id}", response=SchemaOut, auth=None)
def get_poster_template(request, dept_id: int):
    poster = get_object_or_404(Font, id=dept_id)
    return poster


@router.get("/font_sub", auth=None)
def get_font(request, id: int, content: str):
    font = get_object_or_404(Font, id=id)
    try:
        response = requests.get(font.woff)
    except requests.RequestException as e:
        return {'code': -1}
    woff_base64 = base64.b64encode(response.content).decode("utf-8")
    result_string = f"data:font/woff;base64,{woff_base64}"
    return result_string

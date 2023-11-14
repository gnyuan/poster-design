from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from design.models import UImage
from utils.fu_crud import create, delete, retrieve, update
from utils.fu_ninja import FuFilters, MyPagination
from utils.fu_response import FuResponse

router = Router()


class Filters(FuFilters):
    username: str = Field(None, alias="username")
    id: str = Field(None, alias="id")
    category: int = Field(None, alias="cate")
    height: int = Field(None, alias="height")
    width: int = Field(None, alias="width")
    url: str = Field(None, alias="url")


class SchemaIn(ModelSchema):
    class Config:
        model = UImage
        model_exclude = ['id', 'create_datetime', 'update_datetime']


class SchemaOut(ModelSchema):
    class Config:
        model = UImage
        model_fields = "__all__"


@router.post("/user/add_image", response=SchemaOut, auth=None)
@router.post("/uimage", response=SchemaOut, auth=None)
def create_poster_template(request, data: SchemaIn):
    poster = create(request, data, UImage)
    return poster


@router.delete("/uimage/{dept_id}", auth=None)
def delete_poster_template(request, dept_id: int):
    delete(dept_id, UImage)
    return {"success": True}


class SchemaInDel(Schema):
    id: int
    key: Optional[str]

@router.post("/user/image/del", auth=None)
def delete_poster_template(request, data: SchemaInDel):
    delete(data.id, UImage)
    return {"success": True}

@router.put("/uimage/{dept_id}", response=SchemaOut, auth=None)
def update_poster_template(request, dept_id: int, data: SchemaIn):
    poster = update(request, dept_id, data, UImage)
    return poster


@router.get("/uimage", response=List[SchemaOut], auth=None)
@router.get("/user/image", response=List[SchemaOut], auth=None)
@paginate(MyPagination)
def list_poster_template(request, filters: Filters = Query(...)):
    print(filters)
    qs = retrieve(request, UImage, filters)
    return qs


@router.get("/uimage/{dept_id}", response=SchemaOut, auth=None)
def get_poster_template(request, dept_id: int):
    poster = get_object_or_404(UImage, id=dept_id)
    return poster


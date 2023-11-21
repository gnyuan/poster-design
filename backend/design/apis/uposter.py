from typing import List

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from design.models import UPoster
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
        model = UPoster
        model_exclude = ['create_datetime', 'update_datetime']

class SchemaOut(ModelSchema):
    class Config:
        model = UPoster
        model_fields = "__all__"


@router.post("/save", response=SchemaOut, auth=None)
@router.post("/uposter", response=SchemaOut, auth=None)
def create_poster_template(request, data: SchemaIn):
    if data.id: # 更新
        print('更新作品')
        filtered_data = {}
        for k, v in data.__dict__.items():
            if v is None:
                continue
            filtered_data[k] = v
        poster = update(request, data.id, filtered_data, UPoster)
        return poster
    else:
        print('新建作品')
        poster = create(request, data, UPoster)
        return poster


@router.delete("/uposter/{dept_id}", auth=None)
def delete_poster_template(request, dept_id: int):
    delete(dept_id, UPoster)
    return {"success": True}


@router.put("/uposter/{dept_id}", response=SchemaOut, auth=None)
def update_poster_template(request, dept_id: int, data: SchemaIn):
    poster = update(request, dept_id, data, UPoster)
    return poster


@router.get("/uposter", response=List[SchemaOut], auth=None)
@router.get("/my", response=List[SchemaOut], auth=None)
@paginate(MyPagination)
def list_poster_template(request, filters: Filters = Query(...)):
    qs = retrieve(request, UPoster, filters)
    return qs


@router.get("/uposter/{dept_id}", response=SchemaOut, auth=None)
@router.get("/poster", response=SchemaOut, auth=None)
def get_poster_template(request, id: int):
    poster = get_object_or_404(UPoster, id=id)
    return poster

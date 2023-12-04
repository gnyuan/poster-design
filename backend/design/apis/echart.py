from typing import List
from fuadmin.settings import BASE_DIR
import json
import os
from urllib.parse import unquote
from django.http import  HttpResponse

from django.shortcuts import get_object_or_404
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from design.models import Echart
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
    labelName: str = Field(None, alias="labelName")


class SchemaIn(ModelSchema):
    parent_id: int = None

    class Config:
        model = Echart
        model_exclude = ['id', 'create_datetime', 'update_datetime']


class SchemaOut(ModelSchema):
    class Config:
        model = Echart
        model_fields = "__all__"
    # model_fields = []


@router.post("/echart", response=SchemaOut, auth=None)
def create_poster_template(request, data: SchemaIn):
    poster = create(request, data, Echart)
    return poster


@router.delete("/echart/{dept_id}", auth=None)
def delete_poster_template(request, dept_id: int):
    delete(dept_id, Echart)
    return {"success": True}


@router.put("/echart/{dept_id}", response=SchemaOut, auth=None)
def update_poster_template(request, dept_id: int, data: SchemaIn):
    poster = update(request, dept_id, data, Echart)
    return poster


@router.get("/echart", response=List[SchemaOut], auth=None)
@paginate(MyPagination)
def list_poster_template(request, filters: Filters = Query(...)):
    qs = retrieve(request, Echart, filters)
    return qs


@router.get("/echart/{dept_id}", response=SchemaOut, auth=None)
def get_poster_template(request, dept_id: int):
    poster = get_object_or_404(Echart, id=dept_id)
    return poster


@router.get("/echart_option", auth=None)
def get_echart(request, chartId: str):
    echart = get_object_or_404(Echart, chartId = chartId)
    ret = {}
    try:
        if echart.ddcoptions.startswith('http'):
            response = requests.get(echart.ddcoptions)
            ret['option'] = response.content
            response = requests.get(echart.ddcdata)
            ret['data'] = response.content
        else:
            with open(os.path.join(str(BASE_DIR), unquote(echart.ddcoptions.lstrip('/'))), "rb") as fp:
              ret['option'] = json.load(fp)
            with open(os.path.join(str(BASE_DIR), unquote(echart.ddcdata.lstrip('/'))), "rb") as fp:
              ret['data'] = json.load(fp)
    except requests.RequestException as e:
        print('ERROR in echart ddcoptions or ddcdata')
        return {'code': -1}
    return ret

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2022/6/14 17:53
# file: tasks.py
# author: 臧成龙
# QQ: 939589097

from fuadmin.celery import celery_app


@celery_app.task
def test_task():
    print('test')

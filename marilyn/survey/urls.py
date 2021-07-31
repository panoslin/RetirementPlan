#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/31
# IDE: PyCharm
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('report', views.report, name='report'),
]

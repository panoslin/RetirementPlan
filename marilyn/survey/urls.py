#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 2021/7/31
# IDE: PyCharm
from django.urls import path

from . import views

urlpatterns = [
    path('survey/', views.index, name='index'),
    path('392e5faa99df48edbda687cc7571a7b8.txt/', views.wechat_verification, name='wechat_verification'),
    # path('report', views.report, name='report'),
]

# -*- coding: utf-8 -*-
from django.urls import path, re_path
from django.conf.urls import url
from .views import GeoJsonWorldBorderList, GeoJsonWorldBorderDetail, current_datetime, geojson_worldborder_list, geojson_worldborder_detail

urlpatterns = [
    re_path(
        r'geojson/(?P<pk>[0-9]+)/',
        geojson_worldborder_detail,
    ),
    path(
        r'geojson/',
        geojson_worldborder_list,
    ),
    path(r'now', current_datetime),
]
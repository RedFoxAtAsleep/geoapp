# -*- coding: utf-8 -*-

# 准备Django Context实现python manage.py shell效果
import sys
import os
from pathlib import Path
import django
from django.contrib.gis.geos import Point, GEOSGeometry

project = Path(__file__).resolve().parent.parent.parent.parent
# project = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
print('* 项目根目录：', project)
sys.path.append(os.path.join(project))
# 注意不要用os.environ.setdefault()，直接赋值而不是赋默认值
os.environ['DJANGO_SETTINGS_MODULE'] = 'geoapp.settings.base'

django.setup()

from world.models import WorldBorder

# 几何对象的不同表征
print('* 几何对象的不同表征')
# The geometry is in a format known as Well Known Text (WKT) WKT表示几何对象
pnt_wkt = 'POINT(-95.3385 29.7245)'
qs = WorldBorder.objects.filter(mpoly__contains=pnt_wkt)
print('** multipolygon contains point：', qs)

# GEOS geometry object 对象表示集合对象
# from django.contrib.gis.geos import Point
pnt = Point(12.4604, 43.9420)
obj = WorldBorder.objects.get(mpoly__intersects=pnt)
print('** multipolygon intersects point：', obj)


# 自动坐标转换
# Automatic Spatial Transformations
pnt = Point(954158.1, 4215137.1, srid=32140)
pnt = GEOSGeometry('SRID=32140;POINT(954158.1 4215137.1)')
qs = WorldBorder.objects.filter(mpoly__intersects=pnt)
print('* 自动坐标转换', qs[0])


# When using raw queries, you must wrap your geometry fields so that the field value can be recognized by GEOS
# from django.db import connections
# connection = connections['gis']  # if you're querying a non-default database:
# WorldBorder.objects.raw('SELECT id, name, %s as point from world' % (connection.ops.select % 'point'))

# 懒加载 Lazy Geometries
sm = WorldBorder.objects.get(name='San Marino')
pnt = Point(12.4604, 43.9420)
print('* 空间数据的不同表现 multipolygon field：', sm.mpoly)
print('* 空间数据的不同表现 multipolygon field WKT：', sm.mpoly.wkt)
print('* 空间数据的不同表现 multipolygon field WKB (as Python binary buffer)：', sm.mpoly.wkb)
print('* 空间数据的不同表现 multipolygon field WKB GeoJSON：', sm.mpoly.geojson)
print('* 空间对象和空间查询：', sm.mpoly.contains(pnt), pnt.contains(sm.mpoly))











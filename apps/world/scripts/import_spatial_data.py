# -*- coding: utf-8 -*-

# 准备Django Context实现python manage.py shell效果
import sys
import os
import subprocess
import logging
from pathlib import Path
import django
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping


project = Path(__file__).resolve().parent.parent.parent.parent
# project = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
print('* 项目根目录：', project)
sys.path.append(os.path.join(project))
# 注意不要用os.environ.setdefault()，直接赋值而不是赋默认值
os.environ['DJANGO_SETTINGS_MODULE'] = 'geoapp.settings.base'

django.setup()

# Django准备的示例数据 world border
# https://docs.djangoproject.com/en/3.1/ref/contrib/gis/tutorial/#worldborders
world_shp = project / 'apps' / 'world' / 'data' / 'TM_WORLD_BORDERS' /'TM_WORLD_BORDERS-0.3.shp'
print('* 示例shp文件：', world_shp)

# Django Context下得以导入Model
from world.models import WorldBorder
print('* 导入模型', WorldBorder)


# ---------- GDAL Interface 加载查看shp文件（不涉及数据库） ----------


def cli(cmd):
    try:
        os.chdir('/home/executor/app/geoapp/')

        r = subprocess.run(
            cmd,
            shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
        )
        if r.returncode != 0:
            logging.exception('Desc: CLI fail\nException: {}\n'.format(r.stdout))
            return False
        print(r.stdout.decode())
        return True
    except Exception as e:
        logging.exception('Desc: Subprocess fail\nException: {}'.format(e))
        return False


print('* CLI ogrinfo查看shapefiles or other vector data sources元数据metadata')
cmd = 'ogrinfo apps/world/data/TM_WORLD_BORDERS/TM_WORLD_BORDERS-0.3.shp'
print(cli(cmd))
# ogrinfo tells us that the shapefile has one layer,
# and that this layer contains polygon data.
# To find out more, we’ll specify the layer name and use the -so option to get only the important summary information

print('* CLI ogrinfo查看shapefiles or other vector data sources重要的summary information')
cmd = 'ogrinfo -so apps/world/data/TM_WORLD_BORDERS/TM_WORLD_BORDERS-0.3.shp TM_WORLD_BORDERS-0.3'
print(cli(cmd))

# This detailed summary information tells us
# the number of features in the layer (246),
# the geographic bounds of the data,
# the spatial reference system (“SRS WKT”),
# as well as type information for each attribute field.
# For example,
# FIPS: String (2.0) indicates that the FIPS character field has a maximum length of 2.
# Similarly, LON: Real (8.3) is a floating-point field that holds a maximum of 8 digits up to three decimal places.


# GeoDjango’s DataSource interface 打开 world borders shapefile
ds = DataSource(str(world_shp))
print('* GeoDjango接口加载shp文件：', ds)

# Data source objects can have different layers of geospatial features
# however, shapefiles are only allowed to have one layer
print('* shp文件只包含一个图层：', len(ds))


# You can see the layer’s geometry type and how many features it contains
lyr = ds[0]
print('* 图层：', lyr)
print('* 图层特征的几何类型：', lyr.geom_type)
print('* 图层特征的数量：', len(lyr))



# 图层可能携带坐标系信息
srs = lyr.srs
print('* 图层可能携带坐标系信息：', srs, srs.proj4)


# 图层属性
print('* 图层属性：', lyr.fields)
print('* 属性字段 OGR types：', [fld.__name__ for fld in lyr.field_types])

# 遍历图层属性
# Iterate over each feature in the layer and extract information
# from both the feature’s geometry fields(accessed via the geom attribute)
# as well as the feature’s attribute fields (whose values are accessed via get() method):
print('* 遍历图层特征：')
for i, feature in enumerate(lyr):
    if i % 50 == 0:
        print('** {}：'.format(feature.get('NAME')), feature.geom.num_points)
# Layer objects may be sliced
print('* 图层可以被slice：', lyr[:2])
print('* 特征可以被index：', lyr[0])

# Boundary geometries may be exported as WKT and GeoJSON
ftr = lyr[0]
print('* 特征Representation转变：', ftr.geom.wkt)  # Well Known Text (WKT)
print('* 特征Representation转变：', ftr.geom.json)


# ---------- Importing Spatial Data: LayerMapping 导入文件到数据库 ----------

world_mapping = {
    'fips' : 'FIPS',
    'iso2' : 'ISO2',
    'iso3' : 'ISO3',
    'un' : 'UN',
    'name' : 'NAME',
    'area' : 'AREA',
    'pop2005' : 'POP2005',
    'region' : 'REGION',
    'subregion' : 'SUBREGION',
    'lon' : 'LON',
    'lat' : 'LAT',
    'mpoly' : 'MULTIPOLYGON',
}


def run(verbose=True):
    lm = LayerMapping(WorldBorder, str(world_shp), world_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

# run()



# ---------- Auto generate Django model & LayerMapping dictionary 不涉及数据加载和导入----------

# python manage.py ogrinspect [options] <data_source> <model_name> [options]
# python manage.py ogrinspect world/data/TM_WORLD_BORDERS/TM_WORLD_BORDERS-0.3.shp WorldBorderGeneratedByOgrinspect --srid=4326 --mapping --multi

# A few notes about the command-line options given above:

# The --srid=4326 option sets the SRID空间坐标系 for the geographic field.
# The --mapping option tells ogrinspect to also generate a mapping dictionary for use with LayerMapping.
# The --multi option is specified so that the geographic field is a MultiPolygonField instead of just a PolygonField.
# The command produces the following output, which may be copied directly into the models.py of a GeoDjango application.
# The makemigrations and migrate.
# https://docs.djangoproject.com/en/3.1/ref/contrib/gis/tutorial/#introduction

def ogrinspect():
    try:
        os.chdir('/home/executor/app/geoapp/')
        r = subprocess.run(
            'python manage.py ogrinspect apps/world/data/TM_WORLD_BORDERS/TM_WORLD_BORDERS-0.3.shp WorldBorderGeneratedByOgrinspect --srid=4326 --mapping --multi',
            shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
        )

        if r.returncode != 0:
            logging.exception('Desc: CLI fail\nException: {}\n'.format(r.stdout))
            return False
        print(r.stdout.decode())
        return True
    except Exception as e:
        logging.exception('Desc: Subprocess fail\nException: {}'.format(e))
        return False


# ogrinspect()







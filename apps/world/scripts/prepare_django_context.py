# -*- coding: utf-8 -*-
# 准备Django Context实现python manage.py shell效果
import sys
import os
import json
import requests
from pathlib import Path
import django
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

project = Path(__file__).resolve().parent.parent.parent.parent
# project = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))
print('* 项目根目录：', project)
sys.path.append(os.path.join(project))
# 注意不要用os.environ.setdefault()，直接赋值而不是赋默认值
os.environ['DJANGO_SETTINGS_MODULE'] = 'geoapp.settings.base'

django.setup()

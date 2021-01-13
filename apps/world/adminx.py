from django.apps import apps
from django.contrib.gis import admin as gisAdmin
import xadmin
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from .models import WorldBorder
from .forms import WorldBorderForm


# Register your models here.

SPATIAL_FIELD_TYPES = [
    'GeometryField', 'PointField', 'LineStringField',
    'PolygonField', 'MultiPointField', 'MultiLineStringField',
    'MultiPolygonField', 'GeometryCollectionField', 'RasterField'
]
DISPLAY_FIELD_TYPES = [ 'AutoField', 'CharField', 'IntegerField' ]
# 计算属性不可过滤和搜索
# 搜索 模糊查询 字符
SEARCH_FIELD_TYPES = [ 'CharField', 'Field', 'IntegerField' ]
# 过滤 精确查询 字符 数值 日期
FILTER_FIELD_TYPES = [ 'CharField', 'TextField', 'DateField', 'DateTimeField', 'TimeField', 'IntegerField', 'DecimalField', 'FloatField' ]


def get_simple_admin(model):
    name = "simple{}Admin".format(model.__name__)

    all_fields = [field.name for field in model._meta.fields]
    shown_fields = []
    geo_fields = []
    filter_fields = []
    search_fields = []
    for f in model._meta.fields:
        if f.get_internal_type() in DISPLAY_FIELD_TYPES:
            shown_fields.append(f.name)
        if f.get_internal_type() in SPATIAL_FIELD_TYPES:
            geo_fields.append(f.name)
        if f.get_internal_type() in SEARCH_FIELD_TYPES:
            search_fields.append(f.name)
        if f.get_internal_type() in FILTER_FIELD_TYPES:
            filter_fields.append(f.name)

    # admin_model_template = OSMGeoAdminView if len(geo_fields) > 0 else object
    admin_model_template = object
    admin_model = type(
        name,
        (admin_model_template,),
        {

            'refresh_times': [1, 60, 3600, 86400],  # 刷新时间 单位秒
            # 'model_icon', # 导航图标
            # 'hidden_menu',  # 导航隐藏

            'list_display': shown_fields,
            'list_editable': shown_fields,
            'all_fields': all_fields,
            'list_export': [],  # 关闭默认导入导出插件
            'search_fields': search_fields,
            'list_field': filter_fields,
            # 'style_fields': {"info": "ueditor"},  # 集成富文本编辑器
            # 'list_display_links': [],  # 列表页进入详情业 入口字段
            # 'ordering': ["-some_field","other_field"],
            # 'list_per_page': 5,

            # 'show_detail_fields': ['foreign-key'],  # 本身唯一标志和外键
            # 'relfield_style': 'fk-ajax',

            'readonly_fields': ['mpoly'],  # 详情页只读字段
            # 'fields': [],  # 详情业显示字段，fields和exclude互斥
            # 'exclude': [],  # 详情业隐藏字段，fields和exclude互斥
            # 'form',  # 详情页表单定制
            # 'form_layout',  # 详情业排版
        }
    )
    return admin_model


models = apps.get_app_config('world').get_models()
# exclude = ['WorldBorder']
exclude = []
for model in models:
    if model in exclude:
        continue
    xadmin.site.register(model, get_simple_admin(model))


# class WorldBorderAdmin(object):
#     form = WorldBorderForm



























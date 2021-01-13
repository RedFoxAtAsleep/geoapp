from django.contrib import admin
from django.contrib.gis import admin as gisAdmin
from django.apps import apps

# Register your models here.

SPATIAL_FIELD_TYPES = [
    'GeometryField', 'PointField', 'LineStringField',
    'PolygonField', 'MultiPointField', 'MultiLineStringField',
    'MultiPolygonField', 'GeometryCollectionField', 'RasterField'
]
DISPLAY_FIELD_TYPES = [ 'AutoField', 'CharField', 'IntegerField' ]


def get_simple_admin(model):
    name = "simple{}Admin".format(model.__name__)

    shown_fields = []
    geo_fields = set()
    for f in model._meta.fields:
        if f.get_internal_type() in DISPLAY_FIELD_TYPES:
            shown_fields.append(f.name)
        if f.get_internal_type() in SPATIAL_FIELD_TYPES:
            geo_fields.add(f.name)

    admin_model_template = gisAdmin.OSMGeoAdmin if len(geo_fields) > 0 else admin.ModelAdmin

    admin_model = type(
        name,
        (admin_model_template,),
        {'list_display': shown_fields}
    )

    return admin_model


models = apps.get_app_config('world').get_models()
exclude = []
for model in models:
    if model in exclude:
        continue
    admin.site.register(model, get_simple_admin(model))

























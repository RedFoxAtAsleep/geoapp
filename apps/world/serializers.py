# -*- coding: utf-8 -*-
from rest_framework_gis import serializers as gis_serializers
from rest_framework import serializers
from .models import WorldBorder


class WorldBorderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorldBorder
        fields = '__all__'


class WorldBorderGeoFeatureSerializer(gis_serializers.GeoFeatureModelSerializer):
    """ location geo serializer  """

    class Meta:
        model = WorldBorder
        geo_field = 'mpoly'
        fields = '__all__'



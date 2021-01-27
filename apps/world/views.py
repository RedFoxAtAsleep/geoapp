import datetime
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from rest_framework_gis.pagination import GeoJsonPagination
from .serializers import WorldBorderGeoFeatureSerializer, WorldBorderSerializer
from .models import WorldBorder


# Create your views here.
class WorldBorderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = WorldBorder.objects.all().order_by('id')
    serializer_class = WorldBorderSerializer
    permission_classes = [permissions.IsAuthenticated]


class GeoJsonWorldBorderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = WorldBorder.objects.all().order_by('id')
    serializer_class = WorldBorderGeoFeatureSerializer
    permission_classes = [permissions.IsAuthenticated]


class GeoJsonWorldBorderList(generics.ListCreateAPIView):

    model = WorldBorder
    serializer_class = WorldBorderGeoFeatureSerializer
    queryset = WorldBorder.objects.all().order_by('id')
    pagination_class = GeoJsonPagination


geojson_worldborder_list = GeoJsonWorldBorderList.as_view()


class GeoJsonWorldBorderDetail(generics.RetrieveUpdateDestroyAPIView):

    model = WorldBorder
    serializer_class = WorldBorderGeoFeatureSerializer
    queryset = WorldBorder.objects.all()


geojson_worldborder_detail = GeoJsonWorldBorderDetail.as_view()


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)



# -*- coding: utf-8 -*-
# To import the data, use a LayerMapping in a Python script.
# Create a file called load.py inside the world application,
from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import WorldBorder

# Each key in the world_mapping dictionary corresponds to a field in the WorldBorder model.
# The value is the name of the shapefile field that data will be loaded from.
world_mapping = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'mpoly': 'MULTIPOLYGON',
    # Even simple polygons in the shapefile
    # will automatically be converted into collections
    # prior to insertion into the database.
}

# The path to the shapefile is not absolute
# if you move the world application (with data subdirectory) to a different location
# the script will still work.
world_shp = Path(__file__).resolve().parent / 'data' / 'TM_WORLD_BORDERS' / 'TM_WORLD_BORDERS-0.3.shp'


def run(verbose=True):
    lm = LayerMapping(WorldBorder, str(world_shp), world_mapping, transform=False)
    # The transform keyword is set to False because the data in the shapefile
    # does not need to be converted
    # it's already in WGS84(SRID=4326).
    lm.save(strict=True, verbose=verbose)



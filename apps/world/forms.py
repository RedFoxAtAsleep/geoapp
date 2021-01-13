# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json
from django import forms
from django.contrib.gis.admin.widgets import OpenLayersWidget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.forms.widgets import ChoiceWidget, Select
from xadmin.widgets import AdminSelectWidget, AdminTextInputWidget

from .models import WorldBorder


class WorldBorderForm(forms.ModelForm):
    class Meta:
        model = WorldBorder
        exclude = []
        widgets = {
            'mploy': OpenLayersWidget,
        }



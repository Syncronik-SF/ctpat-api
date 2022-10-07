from rest_framework import serializers
from incidence.models import Incidence
from dataclasses import fields

class IncidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidence
        fields = ['id','user','incidencias', 'title','descripcion', 'date','hour','picture']

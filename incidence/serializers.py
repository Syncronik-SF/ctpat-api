from rest_framework import serializers
from incidence.models import Incidence, IncidenceType
from dataclasses import fields

class IncidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidence
        fields = ['id','user', 'embarque', 'incidence_type', 'origen', 'descripcion', 'date','hour','picture']
        
        
class IncidenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidenceType
        fields = '__all__'

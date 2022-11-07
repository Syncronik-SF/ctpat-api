from rest_framework import serializers
from forms.models import Embarque
from incidence.models import Incidence, IncidenceType
from authentication.models import Profile
from dataclasses import fields

class IncidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidence
        fields = ['id','user', 'embarque', 'incidence_type', 'origen', 'descripcion', 'date','hour','picture']
        
class IncidenceDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField('get_user')
    origen_embarque = serializers.SerializerMethodField('get_embarque')
    type_incidence = serializers.SerializerMethodField('get_type_incidence')
    class Meta:
        model = Incidence
        fields = ['id','created_by', 'origen_embarque', 'type_incidence', 'origen', 'descripcion', 'date','hour','picture']
    
    def get_user(self, Incidence):
        pk_incidence = Incidence.pk
        incidence = Incidence.__class__.objects.get(pk=pk_incidence)
        user = incidence.user
        profile = Profile.objects.get(user =user.pk)
        
        data = {"full_name": user.get_full_name_user(), "profile_photo": str(profile.profile_picture)}
        return data
    
    def get_embarque(self, Incidence):
        pk_incidence = Incidence.pk
        incidence = Incidence.__class__.objects.get(pk=pk_incidence)
        embarque = Embarque.objects.get(pk = incidence.embarque.pk)
        data = {"embarque_id": embarque.pk, "destino":embarque.destino.name, "factura": embarque.factura, "sello": embarque.numero_sello}
        return data

    def get_type_incidence(self, Incidence):
        pk_incidence = Incidence.pk
        incidence = Incidence.__class__.objects.get(pk=pk_incidence)
        data = {"id_type": incidence.incidence_type.pk,"type_description": incidence.incidence_type.type}
        return data

class IncidenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidenceType
        fields = '__all__'

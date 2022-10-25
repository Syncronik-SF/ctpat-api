from rest_framework import serializers
from .models import *

class InOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = InOut
        fields = "__all__"
        
        
class RegisterInOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterInOut
        fields = "__all__"
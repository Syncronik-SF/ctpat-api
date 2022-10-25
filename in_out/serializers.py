from rest_framework import serializers
from .models import *

        
class RegisterInOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterInOut
        fields = "__all__"
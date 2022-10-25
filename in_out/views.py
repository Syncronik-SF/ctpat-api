from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import dateparse 

from .models import *

class RegisterInOutAPI(APIView):
    def post(self, request):
        option_id = int(request.data['option_id'])
        full_name = request.data['full_name']
        phone = request.data['phone']
        date = dateparse.parse_date(request.data['date'])
        time = dateparse.parse_time(request.data['time'])
        
        option = InOut.objects.get(id = option_id)
        
        RegisterInOut(option = option, full_name = full_name, phone = phone, date = date, time = time)
        
        return Response({"code": 201, "msg": f"Registro de {option.option} guardado"})
        
        
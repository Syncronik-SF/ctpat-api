from rest_framework import status, generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import dateparse 

from .serializers import RegisterInOutSerializer
from .models import *

class RegisterInAPI(APIView):
    def post(self, request):
        full_name = request.data['full_name']
        phone = request.data['phone']
        dt_in = dateparse.parse_datetime(request.data['dt_in'])
        
        RegisterInOut.objects.create(full_name = full_name, phone = phone, dt_in = dt_in)
        
        return Response({"code": 201, "msg": f"Registro de entrada guardado"}, status=status.HTTP_201_CREATED)
        

class ListAllRegister(generics.ListAPIView):
    
    serializer_class = RegisterInOutSerializer
    def get_queryset(self):
        queryset = RegisterInOut.objects.order_by('dt_in')[::-1]
        return queryset
    
    
class ListRegisterByDate(generics.ListAPIView):
    
    serializer_class = RegisterInOutSerializer
    def get_queryset(self):
        date = self.request.query_params.get('date')
        queryset = RegisterInOut.objects.filter(dt_in__date = date)
        return queryset
    
    
class ListRegisterWithoutOut(generics.ListAPIView):
    
    serializer_class = RegisterInOutSerializer
    def get_queryset(self):
        queryset = RegisterInOut.objects.filter(dt_out=None)
        return queryset


class RegisterOutAPI(APIView):
    def put(self, request, register_id):
        dt_out = dateparse.parse_datetime(request.data['dt_out'])
        
        try:
            register = RegisterInOut.objects.get(id = register_id)
            register.dt_out = dt_out
            register.save()
            data = {"code": 200, "msg": "Registro de salida añadido"}
            code = status.HTTP_200_OK
        except Exception as err:
            print(err)
            data = {"code": 404, "msg": "Registro no encontrado"}
            code = status.HTTP_404_NOT_FOUND
        return Response(data, status = code)
            
            
            

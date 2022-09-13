from .models import Incidence
from incidence.serializers import  IncidenceSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from .models import Incidence

# Create your views here.

@api_view(['POST'])
def incidence_post(request):
    if request.method == 'POST':
        serializer = IncidenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def incidence_update( request,pk ):
    try:
        incidence = Incidence.objects.get( id=pk )
        serializer = IncidenceSerializer(
            instance=incidence, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"datos no validos"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"msg":f"{incidence} no existe"}, status=status.HTTP_400_BAD_REQUEST)   



@api_view(['DELETE'])
def incidence_delete( request, pk ):
    try:
        incidence = Incidence.objects.get( id=pk )
    except:
        return Response( 
            {"msg":"Incidencia no encontrada"}, status=404)       
    if incidence:
        incidence.delete()
    return Response(
        {"msg":"Incidencia borrada correctamente"},status=200)


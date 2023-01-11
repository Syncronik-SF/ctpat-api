from forms.models import Embarque
from .models import Incidence, IncidenceType
from incidence.serializers import  IncidenceDetailSerializer, IncidenceSerializer, IncidenceTypeSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from .models import Incidence
from .sender import generate_message, send_mail
import imghdr
import os
# Create your views here.

from dotenv import load_dotenv

load_dotenv()

SENDER = "mx-ena-it@nidec-ga.com"
PASSWORD = "mtxehlzhotoqfeck"

@api_view(['POST'])
def incidence_post(request):
    if request.method == 'POST':
        serializer = IncidenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            incidence = serializer.data
            embarque = Embarque.objects.get(pk = incidence['embarque'])
            receiver = embarque.autorizado_por.email
            incidence_db = Incidence.objects.get(pk = incidence['id'])
            subject = f"T-Compliance App: Nuevo reporte de incidencia (#{incidence_db.pk})"
           
            content = f"Nuevo reporte de incidencia registrado.\n\nNúmero de caso: #{incidence_db.pk}\nDestino del Embarque: {embarque.destino_name}\nPlacas: {embarque.numero_placas_tractor}\nLinea de Transporte: {embarque.linea_name}\nNombre del Operador: {embarque.operador}\nTipo de Incidencia: {incidence_db.incidence_type.type}\nDetectado en: {incidence_db.origen}\nDescripción del caso: {incidence_db.descripcion}\nReportado por: {incidence_db.user.get_full_name_user()}\nFecha y hora del reporte: {incidence_db.date} {incidence_db.hour}"
            print(content)
            message = generate_message(subject, message = content, receiver="ctpat-mx@nidec-ga.com", sender = "ctpat-mx@nidec-ga.com")
            try:
                image_data = incidence_db.picture.open(mode='rb').read()
                if image_data != None:
                    message.add_attachment(image_data, maintype='image', subtype=imghdr.what(None, image_data))
                else:
                    pass
            except:
                pass
            print(message)
            send_mail(sender = SENDER, password= PASSWORD, receiver = "ctpat-mx@nidec-ga.com", msg = message)
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
        return Response({"msg":"incidence no existe"}, status=status.HTTP_400_BAD_REQUEST)   



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


class Datelist(generics.ListAPIView):
    queryset = Incidence.objects.all()
    serializer_class = IncidenceSerializer
    def get_queryset(self):
      date = self.request.query_params.get('date')
      queryset = Incidence.objects.filter(date=date)
      return queryset


class AllIncidence(generics.ListAPIView):
    queryset = Incidence.objects.all()
    serializer_class = IncidenceDetailSerializer
    def get_queryset(self):
        incidencias = self.request.query_params.get('incidencias')
        queryset = Incidence.objects.all()
        return queryset


@api_view(['GET'])
def incidence_detail(request,pk):
    try:    
        incidence = Incidence.objects.get( id=pk )
        serializer = IncidenceSerializer( incidence )
        
        return Response( serializer.data, status=200)
    except:
        return Response({"msg":"Incidencia no encontrada"}, status=404)
    
    
class ListIncidenceType(generics.ListAPIView):
    
    serializer_class = IncidenceTypeSerializer
    def get_queryset(self):
        return IncidenceType.objects.all()

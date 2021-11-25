import json

from django.shortcuts import render
from django.http.response import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from authentication.models import CustomUser
from .serializer import FormSerializer, FormDetailsSerializer
from .models import Tractor
from forms.models import Formulario

# Create your views here.
def ping(request):
    responseData = {"msg":f"Pong", "status_code":200}
    return HttpResponse(json.dumps(responseData), content_type="application/json")

class CreateForm(APIView):
    def post(self, request):
        user_that_created = request.data['id_user']
        user = CustomUser.objects.get(pk=user_that_created)
        # Create form
        guardia = request.data['guardia']
        operador = request.data['operador']
        created_form = Formulario.objects.create(creado_por = user, guardia = guardia, operador = operador)
        formulario_id = str(created_form.pk)
        formulario = Formulario.objects.get(pk=formulario_id)

        # Create tractor entity
        linea_transporte = request.data['linea_transporte']
        marca_tractor = request.data['marca_tractor']
        numero_placas = request.data['numero_placas']
        created_tractor = Tractor.objects.create(id_formulario = formulario, linea_transporte = linea_transporte, marca_tractor = marca_tractor, numero_placas = numero_placas)
        return Response({"msg":"Form has been created"}, status=status.HTTP_200_OK)

class GetForms(ModelViewSet):
    serializer_class = FormSerializer
    queryset = Formulario.objects.all()

class GetFormDetails(ModelViewSet):
    serializer_class = FormDetailsSerializer
    queryset = Formulario.objects.all()

    def get_serializer_context(self):
        context = super(GetFormDetails, self).get_serializer_context()
        context.update({"request": self.request})
        return context
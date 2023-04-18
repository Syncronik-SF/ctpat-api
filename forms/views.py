import json
import os

from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from authentication.models import CustomUser
from forms.serializer import EmbarqueSerializer, FormDetailsSerializer, GuardiaSerializer, LineaSerializer, DestinoSerializer, ContactoClaveSerializer
from incidence.models import Incidence
#from .serializer import FormSerializer, FormDetailsSerializer
from .models import Embarque, Entrada, Feedback, Guardia, Linea, RevisionCanina, Salida, Destino, ContactoClave, Reporte
from rest_framework_api_key.permissions import HasAPIKey

from rest_framework.decorators import api_view
import requests
from .utils import PDFConverter, convert_boolean_to_yes_or_no, convert_boolean_to_ok_or_no, format_datetime
from .sender.email_sender import EmailSender

from datetime import datetime

SENDER = "mx-ena-it@nidec-ga.com"
PASSWORD = "mtxehlzhotoqfeck"

email_sender = EmailSender(sender=SENDER, password=PASSWORD)
# Create your views here.
def ping(request):
    responseData = {"msg":f"Pong", "status_code":200}
    return HttpResponse(json.dumps(responseData), content_type="application/json")

class CreateEmbarque(APIView):
    # Modelo para manejar la creación del embarque
    def post(self, request):
        user_that_created = request.data['id_user']
        user = CustomUser.objects.get(pk=user_that_created)
        guardia_id = request.data['guardia']
        guardia = Guardia.objects.get(pk=guardia_id)
        operador = request.data['operador']

        no_economico = request.data['no_economico']

        linea_transporte_id = request.data['linea_transporte']
        linea_transporte = Linea.objects.get(pk=linea_transporte_id)

        marca_tractor = request.data['marca_tractor']
        numero_placas_tractor = request.data['numero_placas_tractor']

        linea_de_caja_id = request.data['linea_de_caja']
        linea_de_caja = Linea.objects.get(pk=linea_de_caja_id)
        numero_caja = request.data['numero_caja']
        numero_placas_caja = request.data['numero_placas_caja']

        autorizado_por_id = request.data['autorizado_por']
        autorizado_por = ContactoClave.objects.get(pk=autorizado_por_id)
        #numero_sello = request.data['numero_sello']
        #sello_entregado_a = request.data['sello_entregado_a']
        destino_id = request.data['destino']
        destino = Destino.objects.get(pk=destino_id)

        es_exportacion = request.data['es_exportacion']

        embarque = Embarque.objects.create(creado_por = user, guardia = guardia, operador = operador, linea_transporte = linea_transporte, marca_tractor = marca_tractor, 
        numero_placas_tractor = numero_placas_tractor, no_economico = no_economico, linea_de_caja = linea_de_caja, numero_caja = numero_caja, numero_placas_caja = numero_placas_caja, autorizado_por = autorizado_por,
        destino = destino, es_exportacion = es_exportacion)
        return Response({"msg":"Form embarque been created", "idEmbarque": embarque.pk}, status=status.HTTP_200_OK)


class CreateEntrada(APIView):
    def post(self, request):
        embarque_id = request.data['embarque_id']
        embarque = Embarque.objects.get(pk=embarque_id)
        #numero_cajas_embarque = request.data['numero_cajas_embarque']
        DE_tarjeta_circulacion = request.data['DE_tarjeta_circulacion']
        DE_seguro_obligatorio = request.data['DE_seguro_obligatorio']
        DE_placas_fisicas = request.data['DE_placas_fisicas']
        DE_licencia_federal = request.data['DE_licencia_federal']

        # IN_det_k9 = request.data['IN_det_k9']
        # IN_incumplimiento_cl = request.data['IN_incumplimiento_cl']
        # IN_estado_inconveniente = request.data['IN_estado_inconveniente']

        CGTE_luces_frente = request.data['CGTE_luces_frente']
        CGTE_luces_traseras = request.data['CGTE_luces_traseras']
        CGTE_motor = request.data['CGTE_motor']
        CGTE_tubo_escape = request.data['CGTE_tubo_escape']
        CGTE_exterior_chasis = request.data['CGTE_exterior_chasis']
        CGTE_fugas_aceite = request.data['CGTE_fugas_aceite']
        CGTE_techo_int_ext = request.data['CGTE_techo_int_ext']
        CGTE_puertas_int_ext = request.data['CGTE_puertas_int_ext']
        CGTE_paredes_laterales = request.data['CGTE_paredes_laterales']
        CGTE_parachoques = request.data['CGTE_parachoques']
        CGTE_piso = request.data['CGTE_piso']
        CGTE_patines = request.data['CGTE_patines']
        CGTE_quinta_rueda = request.data['CGTE_quinta_rueda']
        CGTE_tanque_combustible = request.data['CGTE_tanque_combustible']
        CGTE_tanques_aire = request.data['CGTE_tanques_aire']
        CGTE_llantas_rines = request.data['CGTE_llantas_rines']
        CGTE_ejes = request.data['CGTE_ejes']
        CGTE_cabina = request.data['CGTE_cabina']
        CGTE_comopartimientos_herramientas = request.data['CGTE_comopartimientos_herramientas']
        CGTE_agricolas = request.data['CGTE_agricolas']
        CGTE_olores_ext = request.data['CGTE_olores_ext']
        CGTE_humedad = request.data['CGTE_humedad']
        CGTE_obj_sust_ext = request.data['CGTE_obj_sust_ext']

        comentarios_entrada = request.data['comentarios_entrada']
        guardia_id = request.data['guardia_entrada']
        guardia_entrada = Guardia.objects.get(pk=guardia_id)

        created_entrada = Entrada.objects.create(embarque_id = embarque, DE_tarjeta_circulacion = DE_tarjeta_circulacion, DE_seguro_obligatorio = DE_seguro_obligatorio, DE_placas_fisicas = DE_placas_fisicas, DE_licencia_federal = DE_licencia_federal, CGTE_luces_frente = CGTE_luces_frente, CGTE_luces_traseras = CGTE_luces_traseras, CGTE_motor = CGTE_motor, CGTE_tubo_escape = CGTE_tubo_escape, CGTE_exterior_chasis = CGTE_exterior_chasis, CGTE_fugas_aceite = CGTE_fugas_aceite, CGTE_techo_int_ext = CGTE_techo_int_ext, CGTE_puertas_int_ext = CGTE_puertas_int_ext, CGTE_paredes_laterales = CGTE_paredes_laterales, CGTE_parachoques = CGTE_parachoques, CGTE_piso = CGTE_piso, CGTE_patines = CGTE_patines, CGTE_quinta_rueda = CGTE_quinta_rueda, CGTE_tanque_combustible = CGTE_tanque_combustible, CGTE_tanques_aire = CGTE_tanques_aire, CGTE_llantas_rines = CGTE_llantas_rines, CGTE_ejes = CGTE_ejes, CGTE_cabina = CGTE_cabina, CGTE_comopartimientos_herramientas = CGTE_comopartimientos_herramientas, CGTE_agricolas = CGTE_agricolas, CGTE_olores_ext = CGTE_olores_ext, CGTE_humedad = CGTE_humedad, CGTE_obj_sust_ext = CGTE_obj_sust_ext , comentarios_entrada = comentarios_entrada, guardia_entrada = guardia_entrada)
        return Response({"msg":"Form Entrada has been created"}, status=status.HTTP_200_OK)

class CreateRevisionCan(APIView):
    def post(self, request):
        embarque_id = request.data['embarque_id']
        embarque = Embarque.objects.get(pk=embarque_id)
        # Create revisión canina entity
        patio = request.data['patio']
        cliente = request.data['cliente']
        nombre_k9 = request.data['nombre_k9']
        
        PR_defensa = request.data['PR_defensa']
        PR_motor = request.data['PR_motor']
        PR_piso_cabina = request.data['PR_piso_cabina']
        PR_tanque_combustible = request.data['PR_tanque_combustible']
        PR_llantas_rines = request.data['PR_llantas_rines']
        PR_flecha = request.data['PR_flecha']
        PR_cabina = request.data['PR_cabina']
        PR_tanque_aire = request.data['PR_tanque_aire']
        PR_mofles = request.data['PR_mofles']
        PR_equipo_refrigeracion = request.data['PR_equipo_refrigeracion']
        PR_quinta_rueda = request.data['PR_quinta_rueda']
        PR_chasis = request.data['PR_chasis']
        PR_puertas_traseras = request.data['PR_puertas_traseras']
        PR_paredes_techo = request.data['PR_paredes_techo']
        PR_piso_caja = request.data['PR_piso_caja']
        
        #descripcion_hallazgo = request.data['descripcion_hallazgo']
        
        created_revision_canina = RevisionCanina.objects.create(embarque_id = embarque, patio = patio, cliente = cliente, nombre_k9 = nombre_k9, PR_defensa = PR_defensa, PR_motor = PR_motor, PR_piso_cabina = PR_piso_cabina, PR_tanque_combustible = PR_tanque_combustible, PR_llantas_rines = PR_llantas_rines, PR_flecha = PR_flecha, PR_cabina = PR_cabina, PR_tanque_aire = PR_tanque_aire, PR_mofles = PR_mofles, PR_equipo_refrigeracion = PR_equipo_refrigeracion, PR_quinta_rueda = PR_quinta_rueda, PR_chasis = PR_chasis, PR_puertas_traseras = PR_puertas_traseras, PR_paredes_techo = PR_paredes_techo, PR_piso_caja = PR_piso_caja)
        return Response({"msg":"Form Revision Canina has been created"}, status=status.HTTP_200_OK)

class CreateSalida(APIView):
    def post(self, request):
        embarque_id = request.data['embarque_id']
        embarque = Embarque.objects.get(pk=embarque_id)
        DS_doc_embarque = request.data['DS_doc_embarque']
        DS_aut_embarque = request.data['DS_aut_embarque']
        DS_has_sello = request.data['DS_has_sello']
        DS_sello = request.data['DS_sello']
        factura = request.data['factura']
        numero_pallets = request.data['numero_pallets']
        CGTS_luces_frente = request.data['CGTS_luces_frente']
        CGTS_luces_traseras = request.data['CGTS_luces_traseras']
        CGTS_motor = request.data['CGTS_motor']
        CGTS_tubo_escape = request.data['CGTS_tubo_escape']
        CGTS_exterior_chasis = request.data['CGTS_exterior_chasis']
        CGTS_fugas_aceite = request.data['CGTS_fugas_aceite']
        CGTS_techo_int_ext = request.data['CGTS_techo_int_ext']
        CGTS_puertas_int_ext = request.data['CGTS_puertas_int_ext']
        CGTS_paredes_laterales = request.data['CGTS_paredes_laterales']
        CGTS_parachoques = request.data['CGTS_parachoques']
        CGTS_piso = request.data['CGTS_piso']
        CGTS_patines = request.data['CGTS_patines']
        CGTS_quinta_rueda = request.data['CGTS_quinta_rueda']
        CGTS_tanque_combustible = request.data['CGTS_tanque_combustible']
        CGTS_tanques_aire = request.data['CGTS_tanques_aire']
        CGTS_llantas_rines = request.data['CGTS_llantas_rines']
        CGTS_ejes = request.data['CGTS_ejes']
        CGTS_cabina = request.data['CGTS_cabina']
        CGTS_comopartimientos_herramientas = request.data['CGTS_comopartimientos_herramientas']
        CGTS_agricolas = request.data['CGTS_agricolas']
        CGTS_olores_ext = request.data['CGTS_olores_ext']
        CGTS_humedad = request.data['CGTS_humedad']
        CGTS_obj_sust_ext = request.data['CGTS_obj_sust_ext']

        comentarios_salida = request.data['comentarios_salida']
        guardia_id = request.data['guardia_entrada']
        guardia_salida = Guardia.objects.get(pk=guardia_id)

        subject = f"T-Compliance App: Nuevo reporte de Ingreso Vehicular (#{embarque_id})"
        content = f"""Nuevo reporte de Ingreso Vehicular.
            \nNúmero de reporte: #{embarque_id} \nDestino del Embarque: {embarque.destino_name} \nPlacas: {embarque.numero_placas_tractor} \nLinea de Transporte: {embarque.linea_name} \nNombre del Operador: {embarque.operador} \nReportado por: {embarque.creado_por.get_full_name_user()} \nFecha del reporte: {format_datetime(embarque.creado)} \nConsulta el reporte completo: http://ctpat.syncronik.com/api/v1/pdf_view?report-id={embarque_id}
            """
        print(content)
        email_sender.send_mail(receiver="ctpath-view@nidec-ga.com", subject=subject, message=content)
        created_salida = Salida.objects.create(embarque_id = embarque, DS_doc_embarque = DS_doc_embarque, DS_aut_embarque = DS_aut_embarque, DS_has_sello = DS_has_sello, DS_sello = DS_sello, factura = factura, numero_pallets = numero_pallets, CGTS_luces_frente = CGTS_luces_frente, CGTS_luces_traseras = CGTS_luces_traseras, CGTS_motor = CGTS_motor, CGTS_tubo_escape = CGTS_tubo_escape, CGTS_exterior_chasis = CGTS_exterior_chasis, CGTS_fugas_aceite = CGTS_fugas_aceite, CGTS_techo_int_ext = CGTS_techo_int_ext, CGTS_puertas_int_ext = CGTS_puertas_int_ext, CGTS_paredes_laterales = CGTS_paredes_laterales, CGTS_parachoques = CGTS_parachoques, CGTS_piso = CGTS_piso, CGTS_patines = CGTS_patines, CGTS_quinta_rueda = CGTS_quinta_rueda, CGTS_tanque_combustible = CGTS_tanque_combustible, CGTS_tanques_aire = CGTS_tanques_aire, CGTS_llantas_rines = CGTS_llantas_rines, CGTS_ejes = CGTS_ejes, CGTS_cabina = CGTS_cabina, CGTS_comopartimientos_herramientas = CGTS_comopartimientos_herramientas, CGTS_agricolas = CGTS_agricolas, CGTS_olores_ext = CGTS_olores_ext, CGTS_humedad = CGTS_humedad, CGTS_obj_sust_ext = CGTS_obj_sust_ext , comentarios_salida = comentarios_salida, guardia_salida = guardia_salida)
        
        return Response({"msg":"Form Salida has been created"}, status=status.HTTP_200_OK)


# class CreateForm(APIView):
#     def post(self, request):
#         # user_that_created = request.data['id_user']
#         # user = CustomUser.objects.get(pk=user_that_created)
#         # # Create form
#         # guardia = request.data['guardia']
#         # operador = request.data['operador']
#         # created_form = Formulario.objects.create(creado_por = user, guardia = guardia, operador = operador)
#         # formulario_id = str(created_form.pk)
#         # formulario = Formulario.objects.get(pk=formulario_id)

#         # Create tractor entity
#         # linea_transporte = request.data['linea_transporte']
#         # marca_tractor = request.data['marca_tractor']
#         # numero_placas = request.data['numero_placas_tractor']
#         # created_tractor = Tractor.objects.create(id_formulario = formulario, linea_transporte = linea_transporte, marca_tractor = marca_tractor, numero_placas = numero_placas)
        
#         # # Create caja entity
#         # linea_de_caja = request.data['linea_de_caja']
#         # numero_caja = request.data['numero_caja']
#         # placas = request.data['numero_placas_caja']
#         # created_caja = Cajas.objects.create(id_formulario = formulario, linea_de_caja = linea_de_caja, numero_caja = numero_caja, placas = placas)
        
#         # # Create ingreso entity
#         # autorizado_por = request.data['autorizado_por']
#         # factura = request.data['factura']
#         # numero_pallets = request.data['numero_pallets']
#         # numero_sello = request.data['numero_sello']
#         # sello_entregado_a = request.data['sello_entregado_a']
#         # destino = request.data['destino']
#         # es_exportacion = request.data['es_exportacion']
#         # created_ingreso = Ingreso.objects.create(id_formulario=formulario, autorizado_por=autorizado_por, factura=factura, numero_pallets=numero_pallets, numero_sello=numero_sello, sello_entregado_a=sello_entregado_a, destino=destino, es_exportacion=es_exportacion)
        
#         # Create checklist entity
#         # numero_cajas_embarque = request.data['numero_cajas_embarque']
#         # DE_tarjeta_circulacion = request.data['DE_tarjeta_circulacion']
#         # DE_seguro_obligatorio = request.data['DE_seguro_obligatorio']
#         # DE_placas_fisicas = request.data['DE_placas_fisicas']
#         # DE_licencia_federal = request.data['DE_licencia_federal']
#         DS_doc_embarque = request.data['DS_doc_embarque']
#         DS_aut_embarque = request.data['DS_aut_embarque']
#         DS_sello = request.data['DS_sello']
        
#         IN_det_k9 = request.data['IN_det_k9']
#         IN_incumplimiento_cl = request.data['IN_incumplimiento_cl']
#         IN_estado_inconveniente = request.data['IN_estado_inconveniente']
        
#         # CGTS_luces_frente = request.data['CGTE_luces_frente']
#         # CGTE_luces_traseras = request.data['CGTE_luces_traseras']
#         # CGTE_motor = request.data['CGTE_motor']
#         # CGTE_tubo_escape = request.data['CGTE_tubo_escape']
#         # CGTE_exterior_chasis = request.data['CGTE_exterior_chasis']
#         # CGTE_fugas_aceite = request.data['CGTE_fugas_aceite']
#         # CGTE_techo_int_ext = request.data['CGTE_techo_int_ext']
#         # CGTE_puertas_int_ext = request.data['CGTE_puertas_int_ext']
#         # CGTE_paredes_laterales = request.data['CGTE_paredes_laterales']
#         # CGTE_parachoques = request.data['CGTE_parachoques']
#         # CGTE_piso = request.data['CGTE_piso']
#         # CGTE_patines = request.data['CGTE_patines']
#         # CGTE_quinta_rueda = request.data['CGTE_quinta_rueda']
#         # CGTE_tanque_combustible = request.data['CGTE_tanque_combustible']
#         # CGTE_tanques_aire = request.data['CGTE_tanques_aire']
#         # CGTE_llantas_rines = request.data['CGTE_llantas_rines']
#         # CGTE_ejes = request.data['CGTE_ejes']
#         # CGTE_cabina = request.data['CGTE_cabina']
#         # CGTE_comopartimientos_herramientas = request.data['CGTE_comopartimientos_herramientas']
#         # CGTE_agricolas = request.data['CGTE_agricolas']
#         # CGTE_olores_ext = request.data['CGTE_olores_ext']
#         # CGTE_humedad = request.data['CGTE_humedad']
#         # CGTE_obj_sust_ext = request.data['CGTE_obj_sust_ext']
        
#         # CGTS_luces_frente = request.data['CGTS_luces_frente']
#         # CGTS_luces_traseras = request.data['CGTS_luces_traseras']
#         # CGTS_motor = request.data['CGTS_motor']
#         # CGTS_tubo_escape = request.data['CGTS_tubo_escape']
#         # CGTS_exterior_chasis = request.data['CGTS_exterior_chasis']
#         # CGTS_fugas_aceite = request.data['CGTS_fugas_aceite']
#         # CGTS_techo_int_ext = request.data['CGTS_techo_int_ext']
#         # CGTS_puertas_int_ext = request.data['CGTS_puertas_int_ext']
#         # CGTS_paredes_laterales = request.data['CGTS_paredes_laterales']
#         # CGTS_parachoques = request.data['CGTS_parachoques']
#         # CGTS_piso = request.data['CGTS_piso']
#         # CGTS_patines = request.data['CGTS_patines']
#         # CGTS_quinta_rueda = request.data['CGTS_quinta_rueda']
#         # CGTS_tanque_combustible = request.data['CGTS_tanque_combustible']
#         # CGTS_tanques_aire = request.data['CGTS_tanques_aire']
#         # CGTS_llantas_rines = request.data['CGTS_llantas_rines']
#         # CGTS_ejes = request.data['CGTS_ejes']
#         # CGTS_cabina = request.data['CGTS_cabina']
#         # CGTS_comopartimientos_herramientas = request.data['CGTS_comopartimientos_herramientas']
#         # CGTS_agricolas = request.data['CGTS_agricolas']
#         # CGTS_olores_ext = request.data['CGTS_olores_ext']
#         # CGTS_humedad = request.data['CGTS_humedad']
#         # CGTS_obj_sust_ext = request.data['CGTS_obj_sust_ext']
        
#         # comentarios = request.data['comentarios']
#         # guardia_entrada = request.data['guardia_entrada']
#         guardia_salida = request.data['guardia_salida']
        
#         created_checklist = CheckList.objects.create(id_formulario = formulario, numero_cajas_embarque = numero_cajas_embarque, DE_tarjeta_circulacion = DE_tarjeta_circulacion, DE_seguro_obligatorio = DE_seguro_obligatorio, DE_placas_fisicas = DE_placas_fisicas, DE_licencia_federal = DE_licencia_federal, DS_doc_embarque = DS_doc_embarque, DS_aut_embarque = DS_aut_embarque, DS_sello = DS_sello, IN_det_k9 = IN_det_k9, IN_incumplimiento_cl = IN_incumplimiento_cl, IN_estado_inconveniente = IN_estado_inconveniente, CGTE_luces_frente = CGTE_luces_frente, CGTE_luces_traseras = CGTE_luces_traseras, CGTE_motor = CGTE_motor, CGTE_tubo_escape = CGTE_tubo_escape, CGTE_exterior_chasis = CGTE_exterior_chasis, CGTE_fugas_aceite = CGTE_fugas_aceite, CGTE_techo_int_ext = CGTE_techo_int_ext, CGTE_puertas_int_ext = CGTE_puertas_int_ext, CGTE_paredes_laterales = CGTE_paredes_laterales, CGTE_parachoques = CGTE_parachoques, CGTE_piso = CGTE_piso, CGTE_patines = CGTE_patines, CGTE_quinta_rueda = CGTE_quinta_rueda, CGTE_tanque_combustible = CGTE_tanque_combustible, CGTE_tanques_aire = CGTE_tanques_aire, CGTE_llantas_rines = CGTE_llantas_rines, CGTE_ejes = CGTE_ejes, CGTE_cabina = CGTE_cabina, CGTE_comopartimientos_herramientas = CGTE_comopartimientos_herramientas, CGTE_agricolas = CGTE_agricolas, CGTE_olores_ext = CGTE_olores_ext, CGTE_humedad = CGTE_humedad, CGTE_obj_sust_ext = CGTE_obj_sust_ext, CGTS_luces_frente = CGTS_luces_frente, CGTS_luces_traseras = CGTS_luces_traseras, CGTS_motor = CGTS_motor, CGTS_tubo_escape = CGTS_tubo_escape, CGTS_exterior_chasis = CGTS_exterior_chasis, CGTS_fugas_aceite = CGTS_fugas_aceite, CGTS_techo_int_ext = CGTS_techo_int_ext, CGTS_puertas_int_ext = CGTS_puertas_int_ext, CGTS_paredes_laterales = CGTS_paredes_laterales, CGTS_parachoques = CGTS_parachoques, CGTS_piso = CGTS_piso, CGTS_patines = CGTS_patines, CGTS_quinta_rueda = CGTS_quinta_rueda, CGTS_tanque_combustible = CGTS_tanque_combustible, CGTS_tanques_aire = CGTS_tanques_aire, CGTS_llantas_rines = CGTS_llantas_rines, CGTS_ejes = CGTS_ejes, CGTS_cabina = CGTS_cabina, CGTS_comopartimientos_herramientas = CGTS_comopartimientos_herramientas, CGTS_agricolas = CGTS_agricolas, CGTS_olores_ext = CGTS_olores_ext, CGTS_humedad = CGTS_humedad, CGTS_obj_sust_ext = CGTS_obj_sust_ext, comentarios = comentarios, guardia_entrada = guardia_entrada, guardia_salida = guardia_salida)
        
#         # Create revisión canina entity
#         patio = request.data['patio']
#         cliente = request.data['cliente']
#         nombre_k9 = request.data['nombre_k9']
        
#         PR_defensa = request.data['PR_defensa']
#         PR_motor = request.data['PR_motor']
#         PR_piso_cabina = request.data['PR_piso_cabina']
#         PR_tanque_combustible = request.data['PR_tanque_combustible']
#         PR_llantas_rines = request.data['PR_llantas_rines']
#         PR_flecha = request.data['PR_flecha']
#         PR_cabina = request.data['PR_cabina']
#         PR_tanque_aire = request.data['PR_tanque_aire']
#         PR_mofles = request.data['PR_mofles']
#         PR_equipo_refrigeracion = request.data['PR_equipo_refrigeracion']
#         PR_quinta_rueda = request.data['PR_quinta_rueda']
#         PR_chasis = request.data['PR_chasis']
#         PR_puertas_traseras = request.data['PR_puertas_traseras']
#         PR_paredes_techo = request.data['PR_paredes_techo']
#         PR_piso_caja = request.data['PR_piso_caja']
        
#         #descripcion_hallazgo = request.data['descripcion_hallazgo']
        
#         created_revision_canina = RevisionCanina.objects.create(id_formulario = formulario, patio = patio, cliente = cliente, nombre_k9 = nombre_k9, PR_defensa = PR_defensa, PR_motor = PR_motor, PR_piso_cabina = PR_piso_cabina, PR_tanque_combustible = PR_tanque_combustible, PR_llantas_rines = PR_llantas_rines, PR_flecha = PR_flecha, PR_cabina = PR_cabina, PR_tanque_aire = PR_tanque_aire, PR_mofles = PR_mofles, PR_equipo_refrigeracion = PR_equipo_refrigeracion, PR_quinta_rueda = PR_quinta_rueda, PR_chasis = PR_chasis, PR_puertas_traseras = PR_puertas_traseras, PR_paredes_techo = PR_paredes_techo, PR_piso_caja = PR_piso_caja)
        
#         return Response({"msg":"Form has been created"}, status=status.HTTP_200_OK)


# Migrado a nuevo modelo y serializer
class GetForms(ModelViewSet):
    #permission_classes = [HasAPIKey]
    serializer_class = EmbarqueSerializer
    queryset = Embarque.objects.all()

# Pendiente migrar al nuevo serializer
class GetFormDetails(ModelViewSet):
    serializer_class = FormDetailsSerializer
    queryset = Embarque.objects.all()

    def get_serializer_context(self):
        context = super(GetFormDetails, self).get_serializer_context()
        context.update({"request": self.request})
        return context

class GetLastFiveForms(ModelViewSet):
    serializer_class = EmbarqueSerializer
    queryset = Embarque.objects.all().order_by('-id')[:5]

class SaveFeedback(APIView):
    def post(self, request):
        user_that_created = request.data['id_user']
        descripcion = request.data['descripcion']
        user = CustomUser.objects.get(pk=user_that_created)
        feedback = Feedback.objects.create(user=user, descripcion=descripcion)
        return Response({"msg":"¡Feedback recibido!"}, status=status.HTTP_200_OK)

class ListGuardias(generics.ListAPIView):
    
    serializer_class = GuardiaSerializer
    def get_queryset(self):
        return Guardia.objects.all()

class ListLineas(generics.ListAPIView):
    
    serializer_class = LineaSerializer
    def get_queryset(self):
        return Linea.objects.all()

class ListDestinos(generics.ListAPIView):
    
    serializer_class = DestinoSerializer
    def get_queryset(self):
        return Destino.objects.all()

class ListContactosClave(generics.ListAPIView):
    
    serializer_class = ContactoClaveSerializer
    def get_queryset(self):
        return ContactoClave.objects.all()

@api_view(['GET'])
def forms_created(request,pk):
    idForm = Embarque.objects.get(pk=pk)
    response = []
    try:    
        entrada = Entrada.objects.get(embarque_id=idForm )
        print(entrada)
        status_entrada = {"id":1,"reporte": "Revisión de Entrada","isReady": True}
    except:
        status_entrada = {"id":1, "reporte": "Revisión de Entrada","isReady": False, "route": "entrada"}
    response.append(status_entrada)
    # try:    
    #     canina = RevisionCanina.objects.get(embarque_id=idForm )
    #     print(canina)
    #     status_canina = {"id":2, "reporte": "Revisión Canina","isReady": True}
    # except:
    #     status_canina = {"id":2, "reporte": "Revisión Canina","isReady": False, "route": "canina"}
    # response.append(status_canina)
    try:    
        salida = Salida.objects.get(embarque_id=idForm )
        print(salida)
        status_salida = {"id":2,"reporte": "Revisión de Salida","isReady": True}
    except:
        status_salida = {"id":2,"reporte": "Revisión de Salida","isReady": False, "route": "salida"}
    response.append(status_salida)
    return Response(response, status=200)


@api_view(['GET'])
def validate_status_form(request,pk):
    idForm = Embarque.objects.get(pk=pk)
    data = []
    forms_ready = 1
    try:    
        entrada = Entrada.objects.get(embarque_id=idForm )
        print(entrada)
        status_entrada = {"id":1,"reporte": "Revisión de Entrada","isReady": True}
        forms_ready = forms_ready + 1
    except:
        status_entrada = {"id":1, "reporte": "Revisión de Entrada","isReady": False, "route": "entrada"}  
    data.append(status_entrada)
    # try:    
    #     canina = RevisionCanina.objects.get(embarque_id=idForm )
    #     print(canina)
    #     status_canina = {"id":2, "reporte": "Revisión Canina","isReady": True}
    #     forms_ready = forms_ready + 1
    # except:
    #     status_canina = {"id":2, "reporte": "Revisión Canina","isReady": False, "route": "canina"}
        
    # data.append(status_canina)
    try:    
        salida = Salida.objects.get(embarque_id=idForm )
        print(salida)
        status_salida = {"id":2,"reporte": "Revisión de Salida","isReady": True}
        forms_ready = forms_ready + 1
    except:
        status_salida = {"id":2,"reporte": "Revisión de Salida","isReady": False, "route": "salida"}
    data.append(status_salida)

    if forms_ready >= 3:
        response = {"route": "/shipping-details"}
    else:
        response = {"route": "/not-ready"}
    return Response(response, status=200)


class Quantities(APIView):
    
    def get(self, request, date):
        incidencias = len(Incidence.objects.filter(date = date))
        embarques = Embarque.objects.filter(creado__date=date)
        
        entradas = len(Entrada.objects.filter(embarque_id__in = embarques))
        salidas = len(Salida.objects.filter(embarque_id__in = embarques))
        
        embarques = len(embarques)
        
        data = [
            { 
                "label": "Embarques",
                "value": embarques,
                "icon": "assets/camion.gif"
            },
            {
                "label": "Entradas",
                "value": entradas,
                "icon": "assets/entrada.gif"
            },
            {
                "label": "Salidas",
                "value": salidas,
                "icon": "assets/salida.gif"
            },
            {
                "label": "Incidencias",
                "value": incidencias,
                "icon": "assets/alarma.gif"
            }
        ]
        return Response(data, status = status.HTTP_200_OK)
#Opens up page as PDF
class ViewPDF(APIView):
    def get(self, request, *args, **kwargs):
        embarque = Embarque.objects.get(pk=1)
        context = {
            "variable": "pdf_converter",
            "fecha_creacion": embarque.creado,
            "creado_por": embarque.creado_por.get_full_name_user(),
            "operador": embarque.operador,
            "linea_transporte": embarque.linea_name,
            "marca_tractor": embarque.marca_tractor,
            "numero_placas_tractor": embarque.numero_placas_tractor,
            "no_economico": embarque.no_economico,
            "linea_de_caja": embarque.linea_caja_name,
            "numero_caja": embarque.numero_caja,
            "numero_placas_caja": embarque.numero_placas_caja,
            "autorizado_por": embarque.autorizado_por_full_name,
            "destino": embarque.destino_name,
            "es_exportacion": convert_boolean_to_yes_or_no(embarque.es_exportacion),
        }


        pdf_converter = PDFConverter()
        template_path = 'reports/reporte_ingreso.html'  # Reemplazar con la ruta de la plantilla HTML
        output_directory = 'descargas'  # Especificar el directorio de salida
        filename = 'Ingreso-Vehicular-4.pdf'
        pdf_converter.render_and_convert(context, filename, template_path, output_directory)

        return Response({"msg":"Form embarque been created"}, status=status.HTTP_200_OK)

class RenderPDFView(APIView):
    def get(self, request, *args, **kwargs):
        id_shipment = request.GET.get('report-id')
        embarque = Embarque.objects.get(pk=int(id_shipment))
        entrada = Entrada.objects.get(embarque_id = embarque.pk)
        salida = Salida.objects.get(embarque_id = embarque.pk)
        context = {
            "variable": "pdf_converter",
            "fecha_creacion": embarque.creado,
            "creado_por": embarque.creado_por.get_full_name_user(),
            "operador": embarque.operador,
            "linea_transporte": embarque.linea_name,
            "marca_tractor": embarque.marca_tractor,
            "numero_placas_tractor": embarque.numero_placas_tractor,
            "no_economico": embarque.no_economico,
            "linea_de_caja": embarque.linea_caja_name,
            "numero_caja": embarque.numero_caja,
            "numero_placas_caja": embarque.numero_placas_caja,
            "autorizado_por": embarque.autorizado_por_full_name,
            "destino": embarque.destino_name,
            "sello": salida.DS_sello,
            "fecha_salida": salida.fecha_salida,
            "es_exportacion": convert_boolean_to_yes_or_no(embarque.es_exportacion),
            "DE_tarjeta_circulacion": convert_boolean_to_yes_or_no(entrada.DE_tarjeta_circulacion),
            "DE_seguro_obligatorio": convert_boolean_to_yes_or_no(entrada.DE_seguro_obligatorio),
            "DE_licencia_federal": convert_boolean_to_yes_or_no(entrada.DE_licencia_federal),
            "CGTE_luces_frente": convert_boolean_to_ok_or_no(entrada.CGTE_luces_frente),
            "CGTE_luces_traseras": convert_boolean_to_ok_or_no(entrada.CGTE_luces_traseras),
            "CGTE_motor": convert_boolean_to_ok_or_no(entrada.CGTE_motor),
            "CGTE_tubo_escape": convert_boolean_to_ok_or_no(entrada.CGTE_tubo_escape),
            "CGTE_exterior_chasis": convert_boolean_to_ok_or_no(entrada.CGTE_exterior_chasis),
            "CGTE_fugas_aceite": convert_boolean_to_ok_or_no(entrada.CGTE_fugas_aceite),
            "CGTE_techo_int_ext": convert_boolean_to_ok_or_no(entrada.CGTE_techo_int_ext),
            "CGTE_puertas_int_ext": convert_boolean_to_ok_or_no(entrada.CGTE_puertas_int_ext),
            "CGTE_paredes_laterales": convert_boolean_to_ok_or_no(entrada.CGTE_paredes_laterales),
            "CGTE_parachoques": convert_boolean_to_ok_or_no(entrada.CGTE_parachoques),
            "CGTE_piso": convert_boolean_to_ok_or_no(entrada.CGTE_piso),
            "CGTE_patines": convert_boolean_to_ok_or_no(entrada.CGTE_patines),
            "CGTE_quinta_rueda": convert_boolean_to_ok_or_no(entrada.CGTE_quinta_rueda),
            "CGTE_tanque_combustible": convert_boolean_to_ok_or_no(entrada.CGTE_tanque_combustible),
            "CGTE_tanques_aire": convert_boolean_to_ok_or_no(entrada.CGTE_tanques_aire),
            "CGTE_llantas_rines": convert_boolean_to_ok_or_no(entrada.CGTE_llantas_rines),
            "CGTE_ejes": convert_boolean_to_ok_or_no(entrada.CGTE_ejes),
            "CGTE_cabina": convert_boolean_to_ok_or_no(entrada.CGTE_cabina),
            "CGTE_comopartimientos_herramientas": convert_boolean_to_ok_or_no(entrada.CGTE_comopartimientos_herramientas),
            "CGTE_agricolas": convert_boolean_to_ok_or_no(entrada.CGTE_agricolas),
            "CGTE_olores_ext": convert_boolean_to_ok_or_no(entrada.CGTE_olores_ext),
            "CGTE_humedad": convert_boolean_to_ok_or_no(entrada.CGTE_humedad),
            "CGTE_obj_sust_ext": convert_boolean_to_ok_or_no(entrada.CGTE_obj_sust_ext),
            "factura": salida.factura,
            "numero_pallets": salida.numero_pallets
        }

        template_path = 'reports/reporte_ingreso.html'  # Reemplazar con la ruta de la plantilla HTML
        

        return render(request, template_path, context)
        
class CreateDestino(APIView):
    def post(self, request):
        name = request.data['name']

        crate_destino = Destino.objects.create(name=name)
        
        return Response({"msg":"¡Destino agregado!"}, status=status.HTTP_200_OK)

        
class CreatelLinea(APIView):
    def post(self, request):
        name = request.data['name']

        crate_linea = Linea.objects.create(name=name)
        
        return Response({"msg":"¡Línea agregado!"}, status=status.HTTP_200_OK)

class CreateContacto(APIView):
    def post(self, request):
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']

        crate_contacto = ContactoClave.objects.create(first_name=first_name, last_name=last_name, email=email)
        
        return Response({"msg":"¡Contacto agregado!"}, status=status.HTTP_200_OK)


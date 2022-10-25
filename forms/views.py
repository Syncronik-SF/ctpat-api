import json

from django.shortcuts import render
from django.http.response import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from authentication.models import CustomUser
from .serializer import FormSerializer, FormDetailsSerializer
from .models import Tractor, Cajas, Ingreso, CheckList, RevisionCanina
from forms.models import Formulario
from rest_framework_api_key.permissions import HasAPIKey

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
        numero_placas = request.data['numero_placas_tractor']
        created_tractor = Tractor.objects.create(id_formulario = formulario, linea_transporte = linea_transporte, marca_tractor = marca_tractor, numero_placas = numero_placas)
        
        # Create caja entity
        linea_de_caja = request.data['linea_de_caja']
        numero_caja = request.data['numero_caja']
        placas = request.data['numero_placas_caja']
        created_caja = Cajas.objects.create(id_formulario = formulario, linea_de_caja = linea_de_caja, numero_caja = numero_caja, placas = placas)
        
        # Create ingreso entity
        autorizado_por = request.data['autorizado_por']
        factura = request.data['factura']
        numero_pallets = request.data['numero_pallets']
        numero_sello = request.data['numero_sello']
        sello_entregado_a = request.data['sello_entregado_a']
        destino = request.data['destino']
        es_exportacion = request.data['es_exportacion']
        created_ingreso = Ingreso.objects.create(id_formulario=formulario, autorizado_por=autorizado_por, factura=factura, numero_pallets=numero_pallets, numero_sello=numero_sello, sello_entregado_a=sello_entregado_a, destino=destino, es_exportacion=es_exportacion)
        
        # Create checklist entity
        numero_cajas_embarque = request.data['numero_cajas_embarque']
        DE_tarjeta_circulacion = request.data['DE_tarjeta_circulacion']
        DE_seguro_obligatorio = request.data['DE_seguro_obligatorio']
        DE_placas_fisicas = request.data['DE_placas_fisicas']
        DE_licencia_federal = request.data['DE_licencia_federal']
        DS_doc_embarque = request.data['DS_doc_embarque']
        DS_aut_embarque = request.data['DS_aut_embarque']
        DS_sello = request.data['DS_sello']
        
        IN_det_k9 = request.data['IN_det_k9']
        IN_incumplimiento_cl = request.data['IN_incumplimiento_cl']
        IN_estado_inconveniente = request.data['IN_estado_inconveniente']
        
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
        
        comentarios = request.data['comentarios']
        guardia_entrada = request.data['guardia_entrada']
        guardia_salida = request.data['guardia_salida']
        
        created_checklist = CheckList.objects.create(id_formulario = formulario, numero_cajas_embarque = numero_cajas_embarque, DE_tarjeta_circulacion = DE_tarjeta_circulacion, DE_seguro_obligatorio = DE_seguro_obligatorio, DE_placas_fisicas = DE_placas_fisicas, DE_licencia_federal = DE_licencia_federal, DS_doc_embarque = DS_doc_embarque, DS_aut_embarque = DS_aut_embarque, DS_sello = DS_sello, IN_det_k9 = IN_det_k9, IN_incumplimiento_cl = IN_incumplimiento_cl, IN_estado_inconveniente = IN_estado_inconveniente, CGTE_luces_frente = CGTE_luces_frente, CGTE_luces_traseras = CGTE_luces_traseras, CGTE_motor = CGTE_motor, CGTE_tubo_escape = CGTE_tubo_escape, CGTE_exterior_chasis = CGTE_exterior_chasis, CGTE_fugas_aceite = CGTE_fugas_aceite, CGTE_techo_int_ext = CGTE_techo_int_ext, CGTE_puertas_int_ext = CGTE_puertas_int_ext, CGTE_paredes_laterales = CGTE_paredes_laterales, CGTE_parachoques = CGTE_parachoques, CGTE_piso = CGTE_piso, CGTE_patines = CGTE_patines, CGTE_quinta_rueda = CGTE_quinta_rueda, CGTE_tanque_combustible = CGTE_tanque_combustible, CGTE_tanques_aire = CGTE_tanques_aire, CGTE_llantas_rines = CGTE_llantas_rines, CGTE_ejes = CGTE_ejes, CGTE_cabina = CGTE_cabina, CGTE_comopartimientos_herramientas = CGTE_comopartimientos_herramientas, CGTE_agricolas = CGTE_agricolas, CGTE_olores_ext = CGTE_olores_ext, CGTE_humedad = CGTE_humedad, CGTE_obj_sust_ext = CGTE_obj_sust_ext, CGTS_luces_frente = CGTS_luces_frente, CGTS_luces_traseras = CGTS_luces_traseras, CGTS_motor = CGTS_motor, CGTS_tubo_escape = CGTS_tubo_escape, CGTS_exterior_chasis = CGTS_exterior_chasis, CGTS_fugas_aceite = CGTS_fugas_aceite, CGTS_techo_int_ext = CGTS_techo_int_ext, CGTS_puertas_int_ext = CGTS_puertas_int_ext, CGTS_paredes_laterales = CGTS_paredes_laterales, CGTS_parachoques = CGTS_parachoques, CGTS_piso = CGTS_piso, CGTS_patines = CGTS_patines, CGTS_quinta_rueda = CGTS_quinta_rueda, CGTS_tanque_combustible = CGTS_tanque_combustible, CGTS_tanques_aire = CGTS_tanques_aire, CGTS_llantas_rines = CGTS_llantas_rines, CGTS_ejes = CGTS_ejes, CGTS_cabina = CGTS_cabina, CGTS_comopartimientos_herramientas = CGTS_comopartimientos_herramientas, CGTS_agricolas = CGTS_agricolas, CGTS_olores_ext = CGTS_olores_ext, CGTS_humedad = CGTS_humedad, CGTS_obj_sust_ext = CGTS_obj_sust_ext, comentarios = comentarios, guardia_entrada = guardia_entrada, guardia_salida = guardia_salida)
        
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
        
        created_revision_canina = RevisionCanina.objects.create(id_formulario = formulario, patio = patio, cliente = cliente, nombre_k9 = nombre_k9, PR_defensa = PR_defensa, PR_motor = PR_motor, PR_piso_cabina = PR_piso_cabina, PR_tanque_combustible = PR_tanque_combustible, PR_llantas_rines = PR_llantas_rines, PR_flecha = PR_flecha, PR_cabina = PR_cabina, PR_tanque_aire = PR_tanque_aire, PR_mofles = PR_mofles, PR_equipo_refrigeracion = PR_equipo_refrigeracion, PR_quinta_rueda = PR_quinta_rueda, PR_chasis = PR_chasis, PR_puertas_traseras = PR_puertas_traseras, PR_paredes_techo = PR_paredes_techo, PR_piso_caja = PR_piso_caja)
        
        return Response({"msg":"Form has been created"}, status=status.HTTP_200_OK)

class GetForms(ModelViewSet):
    #permission_classes = [HasAPIKey]
    serializer_class = FormSerializer
    queryset = Formulario.objects.all()

class GetFormDetails(ModelViewSet):
    serializer_class = FormDetailsSerializer
    queryset = Formulario.objects.all()

    def get_serializer_context(self):
        context = super(GetFormDetails, self).get_serializer_context()
        context.update({"request": self.request})
        return context

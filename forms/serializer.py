from rest_framework import serializers

from forms.models import Embarque, Entrada, Guardia, RevisionCanina, Salida

#from .models import CheckList, Formulario, Ingreso, RevisionCanina, Tractor, Cajas

import pdb
class EmbarqueSerializer(serializers.ModelSerializer):
    pasos = serializers.SerializerMethodField('get_conciliacion')
    class Meta:
        model = Embarque
        fields = ['pasos','pk','creado_por', 'guardia', 'operador', 'creado', 'modificado', 'linea_transporte','marca_tractor', 'numero_placas_tractor', 'no_economico', 'linea_de_caja', 'numero_caja', 'numero_placas_caja', 'autorizado_por', 'factura', 'numero_pallets', 'numero_sello', 'sello_entregado_a', 'destino', 'es_exportacion']
        
    def get_conciliacion(self, Embarque):
        idEmbarque = Embarque.pk
        embarque = Embarque.__class__.objects.get(pk = idEmbarque)
        pasos_completados = 1
        try:
            entrada = Entrada.objects.get(embarque_id=embarque.pk)
            print(entrada)
            pasos_completados = pasos_completados + 1
        except:
            pass
        # try:
        #     canina = RevisionCanina.objects.get(embarque_id = embarque.pk)
        #     pasos_completados = pasos_completados + 1
        # except:
        #     pass
        try:    
            entrada = Salida.objects.get(embarque_id=embarque.pk)
            pasos_completados = pasos_completados + 1
        except:
            pass
        return pasos_completados
# class FormSerializer(serializers.ModelSerializer):

#     creado_por = serializers.SerializerMethodField('get_full_name')
#     destino = serializers.SerializerMethodField('get_destiny')
#     placas_tractor = serializers.SerializerMethodField('get_placas_tractor')
#     placas_caja = serializers.SerializerMethodField('get_placas_caja')
#     isOk = serializers.SerializerMethodField('get_is_ok')

#     class Meta:
#         model = Formulario
#         fields = ['pk', 'destino', 'placas_tractor', 'placas_caja', 'guardia', 'operador', 'creado', 'modificado', 'creado_por', 'isOk']
    
#     def get_full_name(self, Formulario):
#         creado_por = Formulario.creado_por
#         return str(creado_por)
    
#     def get_destiny(self, Formulario):
#         formulario_actual = Formulario.pk
#         ingreso = Ingreso.objects.get(id_formulario = formulario_actual)
#         destino = ingreso.destino
#         return str(destino)
    
#     def get_placas_tractor(self, Formulario):
#         formulario_actual = Formulario.pk
#         tractor = Tractor.objects.get(id_formulario = formulario_actual)
#         numero_placas = tractor.numero_placas
#         return str(numero_placas)

#     def get_placas_caja(self, Formulario):
#         formulario_actual = Formulario.pk
#         cajas = Cajas.objects.get(id_formulario = formulario_actual)
#         numero_caja = cajas.numero_caja
#         return str(numero_caja)

#     def get_is_ok(self, Formulario):
#         return True

class FormDetailsSerializer(serializers.ModelSerializer):
    resumen = serializers.SerializerMethodField('get_resumen')
    entrada = serializers.SerializerMethodField('get_data_entrada')
    salida = serializers.SerializerMethodField('get_data_salida')
    #form = serializers.SerializerMethodField('get_data_form')
    #tractor = serializers.SerializerMethodField('get_data_tractor')
    #cajas = serializers.SerializerMethodField('get_data_cajas')
    #ingreso = serializers.SerializerMethodField('get_data_ingreso')
    #checklist = serializers.SerializerMethodField('get_data_checklist')
    #revision_canina = serializers.SerializerMethodField('get_data_revision_canina')

    class Meta:
        model = Embarque
        fields = ['resumen', 'entrada', 'salida']

    def get_me(self, Embarque):
        shipment = self.context['request'].GET.get('shipment')
        return str(shipment)

    def get_resumen(self, Embarque):
        shipment = self.context['request'].GET.get('shipment')
        form = Embarque.__class__.objects.get(pk = shipment)
        # tractor = Tractor.objects.get(id_formulario = form.pk)
        # cajas = Cajas.objects.get(id_formulario = form.pk)
        # ingreso = Ingreso.objects.get(id_formulario = form.pk)
        # checklist = CheckList.objects.get(id_formulario = form.pk)
        data = {
            "ID Formulario" : form.pk,
            "Creado por": form.creado_por.get_full_name_user(),
            "Guardia": form.guardia.user.get_full_name_user(),
            "Operador": form.operador,
            "Creado": form.creado,
            "Modificado": form.modificado,
            "Está ok": True,
            "Línea de transporte de tractor": form.linea_transporte,
            "Marca de tractor": form.marca_tractor,
            "Número de placas de tractor": form.numero_placas_tractor,
            "Número económico de tractor": form.no_economico,
            "Línea de caja": form.linea_de_caja,
            "Número de caja": form.numero_caja,
            "Placas de caja": form.numero_placas_caja,
            "Autorizado por": form.autorizado_por,
            "Factura": form.factura,
            "Número de pallets": form.numero_pallets,
            "Número de sello": form.numero_sello,
            "Sello entregado a": form.sello_entregado_a,
            "Destino": form.destino,
            "Es exportación a EU": form.es_exportacion,
        }
        return data


    def get_entrada(self, Embarque):
        shipment = self.context['request'].GET.get('shipment')
        form = Embarque.__class__.objects.get(pk = shipment)
        try:
            ingreso = Entrada.objects.get(embarque_id = form.pk)
            data =  {
                "autorizado_por": ingreso.autorizado_por,
                "factura": ingreso.factura,
                "numero_pallets": ingreso.numero_pallets,
                "numero_sello": ingreso.numero_sello,
                "sello_entregado_a": ingreso.sello_entregado_a,
                "destino": ingreso.destino,
                "es_exportacion": ingreso.es_exportacion,
            }
        except:
            data = {"Sin datos": "No existe registro de entrada"}
        return data
    
    def get_data_entrada(self, Embarque):
        shipment = self.context['request'].GET.get('shipment')
        form = Embarque.__class__.objects.get(pk = shipment)
        try:
            entrada = Entrada.objects.get(embarque_id = form.pk)
            salida = Salida.objects.get(embarque_id = form.pk)
            data = {
            
            "Tarjeta de circulación": entrada.DE_tarjeta_circulacion,
            "Seguro obligatorio": entrada.DE_seguro_obligatorio,
            "Placas físicas de circulación": entrada.DE_placas_fisicas,
            "Licencia federal": entrada.DE_licencia_federal,
            #"Shiping, documentación de embarque": checklist.DS_doc_embarque,
            #"Autorización de salida por embarques": checklist.DS_aut_embarque,
            #"Detección K9": checklist.IN_det_k9,
            #"Inclumpimiento CheckList": checklist.IN_incumplimiento_cl,
            #"Estado inconveniente del transportista": checklist.IN_estado_inconveniente,
            "Entrada: Luces del frente": entrada.CGTE_luces_frente,
            "Entrada: Luces traseras": entrada.CGTE_luces_traseras,
            "Entrada: Motor": entrada.CGTE_motor,
            "Entrada: Tubo de escape": entrada.CGTE_tubo_escape,
            "Entrada: Exterior chasis": entrada.CGTE_exterior_chasis,
            "Entrada: Fugas de aceite": entrada.CGTE_fugas_aceite,
            "Entrada: Techo interior/exterior": entrada.CGTE_techo_int_ext,
            "Entrada: Puertas interiores/exteriores": entrada.CGTE_puertas_int_ext,
            "Entrada: Paredes laterales": entrada.CGTE_paredes_laterales,
            "Entrada: Parachoques": entrada.CGTE_parachoques,
            "Entrada: Piso": entrada.CGTE_piso,
            "Entrada: Patines": entrada.CGTE_patines,
            "Entrada: Quinta rueda": entrada.CGTE_quinta_rueda,
            "Entrada: Tanque de combustible": entrada.CGTE_tanque_combustible,
            "Entrada: Tanques de aire": entrada.CGTE_tanques_aire,
            "Entrada: Llantas y rines": entrada.CGTE_llantas_rines,
            "Entrada: Ejes": entrada.CGTE_ejes,
            "Entrada: Cabina": entrada.CGTE_cabina,
            "Entrada: Compartimiento herramientas": entrada.CGTE_comopartimientos_herramientas,
            "Entrada: Agrícolas (Plagas)": entrada.CGTE_agricolas,
            "Entrada: Olores extraños": entrada.CGTE_olores_ext,
            "Entrada: Humedad": entrada.CGTE_humedad,
            "Entrada: Objetos o sustancias extrañas": entrada.CGTE_obj_sust_ext,

            "Salida: Luces del frente": salida.CGTS_luces_frente,
            "Salida: Luces traseras": salida.CGTS_luces_traseras,
            "Salida: Motor": salida.CGTS_motor,
            "Salida: Tubo de escape": salida.CGTS_tubo_escape,
            "Salida: Exterior chasis": salida.CGTS_exterior_chasis,
            "Salida: Fugas de aceite": salida.CGTS_fugas_aceite,
            "Salida: Techo interior/exterior": salida.CGTS_techo_int_ext,
            "Salida: Puertas interiores/exteriores": salida.CGTS_puertas_int_ext,
            "Salida: Paredes laterales": salida.CGTS_paredes_laterales,
            "Salida: Parachoques": salida.CGTS_parachoques,
            "Salida: Piso": salida.CGTS_piso,
            "Salida: Patines": salida.CGTS_patines,
            "Salida: Quinta rueda": salida.CGTS_quinta_rueda,
            "Salida: Tanque de combustible": salida.CGTS_tanque_combustible,
            "Salida: Tanques de aire": salida.CGTS_tanques_aire,
            "Salida: Llantas y rines": salida.CGTS_llantas_rines,
            "Salida: Ejes": salida.CGTS_ejes,
            "Salida: Cabina": salida.CGTS_cabina,
            "Salida: Compartimiento herramientas": salida.CGTS_comopartimientos_herramientas,
            "Salida: Agrícolas (Plagas)": salida.CGTS_agricolas,
            "Salida: Olores extraños": salida.CGTS_olores_ext,
            "Salida: Humedad": salida.CGTS_humedad,
            "Salida: Objetos o sustancias extrañas": salida.CGTS_obj_sust_ext,

        }
        except:
            data = {"Sin datos": "No existe registros de entrada"}
        return data

    def get_data_salida(self, Embarque):
        shipment = self.context['request'].GET.get('shipment')
        form = Embarque.__class__.objects.get(pk = shipment)
        try:
            entrada = Entrada.objects.get(embarque_id = form.pk)
            salida = Salida.objects.get(embarque_id = form.pk)
            data = {
            "Salida: Luces del frente": salida.CGTS_luces_frente,
            "Salida: Luces traseras": salida.CGTS_luces_traseras,
            "Salida: Motor": salida.CGTS_motor,
            "Salida: Tubo de escape": salida.CGTS_tubo_escape,
            "Salida: Exterior chasis": salida.CGTS_exterior_chasis,
            "Salida: Fugas de aceite": salida.CGTS_fugas_aceite,
            "Salida: Techo interior/exterior": salida.CGTS_techo_int_ext,
            "Salida: Puertas interiores/exteriores": salida.CGTS_puertas_int_ext,
            "Salida: Paredes laterales": salida.CGTS_paredes_laterales,
            "Salida: Parachoques": salida.CGTS_parachoques,
            "Salida: Piso": salida.CGTS_piso,
            "Salida: Patines": salida.CGTS_patines,
            "Salida: Quinta rueda": salida.CGTS_quinta_rueda,
            "Salida: Tanque de combustible": salida.CGTS_tanque_combustible,
            "Salida: Tanques de aire": salida.CGTS_tanques_aire,
            "Salida: Llantas y rines": salida.CGTS_llantas_rines,
            "Salida: Ejes": salida.CGTS_ejes,
            "Salida: Cabina": salida.CGTS_cabina,
            "Salida: Compartimiento herramientas": salida.CGTS_comopartimientos_herramientas,
            "Salida: Agrícolas (Plagas)": salida.CGTS_agricolas,
            "Salida: Olores extraños": salida.CGTS_olores_ext,
            "Salida: Humedad": salida.CGTS_humedad,
            "Salida: Objetos o sustancias extrañas": salida.CGTS_obj_sust_ext,

        }
        except:
            data = {"Sin datos": "No existe registros de salida"}
        return data
    
    

    # def get_data_revision_canina(self, Embarque):
    #     shipment = self.context['request'].GET.get('shipment')
    #     form = Embarque.__class__.objects.get(pk = shipment)
    #     try:
    #         revision_can = RevisionCanina.objects.get(embarque_id = form.pk)
    #         data =  {
    #         "Patio": revision_can.patio,
    #         "Cliente": revision_can.cliente,
    #         "Nombre del K9": revision_can.nombre_k9,
    #         "Defensa": revision_can.PR_defensa,
    #         "Motor": revision_can.PR_motor,
    #         "Piso de cabina": revision_can.PR_piso_cabina,
    #         "Tanque de Combustible": revision_can.PR_tanque_combustible,
    #         "Llantas y Rines": revision_can.PR_llantas_rines,
    #         "Flecha": revision_can.PR_flecha,
    #         "Cabina": revision_can.PR_cabina,
    #         "Tanque de aire": revision_can.PR_tanque_aire,
    #         "Mofles/Escape": revision_can.PR_mofles,
    #         "Equipo de refigeración": revision_can.PR_equipo_refrigeracion,
    #         "Quinta Rueda": revision_can.PR_quinta_rueda,
    #         "Chasis": revision_can.PR_chasis,
    #         "Puertas traseras": revision_can.PR_puertas_traseras,
    #         "Paredes/Techo": revision_can.PR_paredes_techo,
    #         "Piso de la caja": revision_can.PR_piso_caja,
    #         #"descripcion_hallazgo": revision_can.descripcion_hallazgo,
    #     }
    #     except:
    #         data = {"Sin datos": "No existe registro de revision canina"}
    #     return data


class GuardiaSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')
    class Meta:
        model = Guardia
        fields = ["pk", 'full_name']

    def get_full_name(self, Guardia):
        guardia = Guardia.user
        return str(guardia)
        

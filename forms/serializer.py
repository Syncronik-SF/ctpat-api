from rest_framework import serializers

from .models import CheckList, Formulario, Ingreso, Tractor, Cajas

class FormSerializer(serializers.ModelSerializer):

    creado_por = serializers.SerializerMethodField('get_full_name')
    destino = serializers.SerializerMethodField('get_destiny')
    placas_tractor = serializers.SerializerMethodField('get_placas_tractor')
    placas_caja = serializers.SerializerMethodField('get_placas_caja')

    class Meta:
        model = Formulario
        fields = ['pk', 'destino', 'placas_tractor', 'placas_caja', 'guardia', 'operador', 'creado', 'modificado', 'creado_por',]
    
    def get_full_name(self, Formulario):
        creado_por = Formulario.creado_por
        return str(creado_por)
    
    def get_destiny(self, Formulario):
        formulario_actual = Formulario.pk
        ingreso = Ingreso.objects.get(id_formulario = formulario_actual)
        destino = ingreso.destino
        return str(destino)
    
    def get_placas_tractor(self, Formulario):
        formulario_actual = Formulario.pk
        tractor = Tractor.objects.get(id_formulario = formulario_actual)
        numero_placas = tractor.numero_placas
        return str(numero_placas)

    def get_placas_caja(self, Formulario):
        formulario_actual = Formulario.pk
        cajas = Cajas.objects.get(id_formulario = formulario_actual)
        numero_caja = cajas.numero_caja
        return str(numero_caja)

class FormDetailsSerializer(serializers.ModelSerializer):
    form = serializers.SerializerMethodField('get_data_form')
    tractor = serializers.SerializerMethodField('get_data_tractor')
    cajas = serializers.SerializerMethodField('get_data_cajas')
    ingreso = serializers.SerializerMethodField('get_data_ingreso')
    checklist = serializers.SerializerMethodField('get_data_checklist')

    class Meta:
        model = Formulario
        fields = ['form', 'tractor', 'cajas', 'ingreso', 'checklist']

    def get_me(self, Formulario):
        me = self.context['request'].GET.get('me')
        return str(me)
    
    def get_data_form(self, Formulario):
        me = self.context['request'].GET.get('me')
        form = Formulario.__class__.objects.get(pk = me)
        tractor = Tractor.objects.get(id_formulario = form.pk)
        data = {
            "form_id" : form.pk,
            "creado_por": form.creado_por.get_full_name_user(),
            "guardia": form.guardia,
            "operador": form.operador,
            "creado": form.creado,
            "modificado": form.modificado,
        }
        return data
    
    def get_data_tractor(self, Formulario):
        me = self.context['request'].GET.get('me')
        form = Formulario.__class__.objects.get(pk = me)
        tractor = Tractor.objects.get(id_formulario = form.pk)
        data =  {
                "linea_transporte": tractor.linea_transporte,
                "marca_tractor": tractor.marca_tractor,
                "numero_placas": tractor.numero_placas,
                "no_economico": tractor.no_economico,
        }
        return data

    def get_data_cajas(self, Formulario):
        me = self.context['request'].GET.get('me')
        form = Formulario.__class__.objects.get(pk = me)
        cajas = Cajas.objects.get(id_formulario = form.pk)
        data =  {
                "linea_de_caja": cajas.linea_de_caja,
                "numero_caja": cajas.numero_caja,
                "placas": cajas.placas,
        }
        return data

    def get_data_ingreso(self, Formulario):
        me = self.context['request'].GET.get('me')
        form = Formulario.__class__.objects.get(pk = me)
        ingreso = Ingreso.objects.get(id_formulario = form.pk)
        data =  {
                "autorizado_por": ingreso.autorizado_por,
                "factura": ingreso.factura,
                "numero_pallets": ingreso.numero_pallets,
                "numero_sello": ingreso.numero_sello,
                "sello_entregado_a": ingreso.sello_entregado_a,
                "destino": ingreso.destino,
                "es_exportacion": ingreso.es_exportacion,
        }
        return data
    
    def get_data_checklist(self, Formulario):
        me = self.context['request'].GET.get('me')
        form = Formulario.__class__.objects.get(pk = me)
        checklist = CheckList.objects.get(id_formulario = form.pk)
        data = {
            "numero_cajas_embarque": checklist.numero_cajas_embarque,
            "DE_tarjeta_circulacion": checklist.DE_tarjeta_circulacion,
            "DE_seguro_obligatorio": checklist.DE_seguro_obligatorio,
            "DE_placas_fisicas": checklist.DE_placas_fisicas,
            "DE_licencia_federal": checklist.DE_licencia_federal,
            "DS_doc_embarque": checklist.DS_doc_embarque,
            "DS_aut_embarque": checklist.DS_aut_embarque,
            "DS_sello": checklist.DS_sello,
            "IN_det_k9": checklist.IN_det_k9,
            "IN_incumplimiento_cl": checklist.IN_incumplimiento_cl,
            "IN_estado_inconveniente": checklist.IN_estado_inconveniente,
            "CGTE_luces_frente": checklist.CGTE_luces_frente,
            "CGTE_luces_traseras": checklist.CGTE_luces_traseras,
            "CGTE_motor": checklist.CGTE_motor,
            "CGTE_tubo_escape": checklist.CGTE_tubo_escape,
            "CGTE_exterior_chasis": checklist.CGTE_exterior_chasis,
            "CGTE_fugas_aceite": checklist.CGTE_fugas_aceite,
            "CGTE_techo_int_ext": checklist.CGTE_techo_int_ext,
            "CGTE_puertas_int_ext": checklist.CGTE_puertas_int_ext,
            "CGTE_paredes_laterales": checklist.CGTE_paredes_laterales,
            "CGTE_parachoques": checklist.CGTE_parachoques,
            "CGTE_piso": checklist.CGTE_piso,
            "CGTE_patines": checklist.CGTE_patines,
            "CGTE_quinta_rueda": checklist.CGTE_quinta_rueda,
            "CGTE_tanque_combustible": checklist.CGTE_tanque_combustible,
            "CGTE_tanques_aire": checklist.CGTE_tanques_aire,
            "CGTE_llantas_rines": checklist.CGTE_llantas_rines,
            "CGTE_ejes": checklist.CGTE_ejes,
            "CGTE_cabina": checklist.CGTE_cabina,
            "CGTE_comopartimientos_herramientas": checklist.CGTE_comopartimientos_herramientas,
            "CGTE_agricolas": checklist.CGTE_agricolas,
            "CGTE_olores_ext": checklist.CGTE_olores_ext,
            "CGTE_humedad": checklist.CGTE_humedad,
            "CGTE_obj_sust_ext": checklist.CGTE_obj_sust_ext,

            "CGTS_luces_frente": checklist.CGTS_luces_frente,
            "CGTS_luces_traseras": checklist.CGTS_luces_traseras,
            "CGTS_motor": checklist.CGTS_motor,
            "CGTS_tubo_escape": checklist.CGTS_tubo_escape,
            "CGTS_exterior_chasis": checklist.CGTS_exterior_chasis,
            "CGTS_fugas_aceite": checklist.CGTS_fugas_aceite,
            "CGTS_techo_int_ext": checklist.CGTS_techo_int_ext,
            "CGTS_puertas_int_ext": checklist.CGTS_puertas_int_ext,
            "CGTS_paredes_laterales": checklist.CGTS_paredes_laterales,
            "CGTS_parachoques": checklist.CGTS_parachoques,
            "CGTS_piso": checklist.CGTS_piso,
            "CGTS_patines": checklist.CGTS_patines,
            "CGTS_quinta_rueda": checklist.CGTS_quinta_rueda,
            "CGTS_tanque_combustible": checklist.CGTS_tanque_combustible,
            "CGTS_tanques_aire": checklist.CGTS_tanques_aire,
            "CGTS_llantas_rines": checklist.CGTS_llantas_rines,
            "CGTS_ejes": checklist.CGTS_ejes,
            "CGTS_cabina": checklist.CGTS_cabina,
            "CGTS_comopartimientos_herramientas": checklist.CGTS_comopartimientos_herramientas,
            "CGTS_agricolas": checklist.CGTS_agricolas,
            "CGTS_olores_ext": checklist.CGTS_olores_ext,
            "CGTS_humedad": checklist.CGTS_humedad,
            "CGTS_obj_sust_ext": checklist.CGTS_obj_sust_ext,

            "comentarios" : checklist.comentarios,
            "guardia_entrada": checklist.guardia_entrada,
            "guardia_salida": checklist.guardia_salida,

        }
        return data
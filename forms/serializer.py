from rest_framework import serializers

from .models import CheckList, Formulario, Ingreso, RevisionCanina, Tractor, Cajas

class FormSerializer(serializers.ModelSerializer):

    creado_por = serializers.SerializerMethodField('get_full_name')
    destino = serializers.SerializerMethodField('get_destiny')
    placas_tractor = serializers.SerializerMethodField('get_placas_tractor')
    placas_caja = serializers.SerializerMethodField('get_placas_caja')
    isOk = serializers.SerializerMethodField('get_is_ok')

    class Meta:
        model = Formulario
        fields = ['pk', 'destino', 'placas_tractor', 'placas_caja', 'guardia', 'operador', 'creado', 'modificado', 'creado_por', 'isOk']
    
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

    def get_is_ok(self, Formulario):
        return True

class FormDetailsSerializer(serializers.ModelSerializer):
    resumen = serializers.SerializerMethodField('get_resumen')
    #form = serializers.SerializerMethodField('get_data_form')
    #tractor = serializers.SerializerMethodField('get_data_tractor')
    #cajas = serializers.SerializerMethodField('get_data_cajas')
    #ingreso = serializers.SerializerMethodField('get_data_ingreso')
    checklist = serializers.SerializerMethodField('get_data_checklist')
    revision_canina = serializers.SerializerMethodField('get_data_revision_canina')

    class Meta:
        model = Formulario
        fields = ['resumen', 'checklist', 'revision_canina']

    def get_me(self, Formulario):
        shipment = self.context['request'].GET.get('shipment')
        return str(shipment)

    def get_resumen(self, Formulario):
        shipment = self.context['request'].GET.get('shipment')
        form = Formulario.__class__.objects.get(pk = shipment)
        tractor = Tractor.objects.get(id_formulario = form.pk)
        cajas = Cajas.objects.get(id_formulario = form.pk)
        ingreso = Ingreso.objects.get(id_formulario = form.pk)
        checklist = CheckList.objects.get(id_formulario = form.pk)
        data = {
            "ID Formulario" : form.pk,
            "Creado por": form.creado_por.get_full_name_user(),
            "Guardia": form.guardia,
            "Operador": form.operador,
            "Creado": form.creado,
            "Modificado": form.modificado,
            "Está ok": True,
            "Línea de transporte de tractor": tractor.linea_transporte,
            "Marca de tractor": tractor.marca_tractor,
            "Número de placas de tractor": tractor.numero_placas,
            "Número económico de tractor": tractor.no_economico,
            "Línea de caja": cajas.linea_de_caja,
            "Número de caja": cajas.numero_caja,
            "Placas de caja": cajas.placas,
            "Autorizado por": ingreso.autorizado_por,
            "Factura": ingreso.factura,
            "Número de pallets": ingreso.numero_pallets,
            "Número de sello": ingreso.numero_sello,
            "Sello entregado a": ingreso.sello_entregado_a,
            "Destino": ingreso.destino,
            "Sello": checklist.DS_sello,
            "Número de cajas de embarque": checklist.numero_cajas_embarque,
            "Comentarios" : checklist.comentarios,
            "Guardia de Entrada": checklist.guardia_entrada,
            "Guardia de Salida": checklist.guardia_salida,
            "Es exportación a EU": ingreso.es_exportacion,
        }
        return data
    
    def get_data_form(self, Formulario):
        shipment = self.context['request'].GET.get('shipment')
        form = Formulario.__class__.objects.get(pk = shipment)
        tractor = Tractor.objects.get(id_formulario = form.pk)
        data = {
            "form_id" : form.pk,
            "creado_por": form.creado_por.get_full_name_user(),
            "guardia": form.guardia,
            "operador": form.operador,
            "creado": form.creado,
            "modificado": form.modificado,
            "isOk": True
        }
        return data
    
    def get_data_tractor(self, Formulario):
        shipment = self.context['request'].GET.get('shipment')
        form = Formulario.__class__.objects.get(pk = shipment)
        tractor = Tractor.objects.get(id_formulario = form.pk)
        data =  {
                "linea_transporte": tractor.linea_transporte,
                "marca_tractor": tractor.marca_tractor,
                "numero_placas": tractor.numero_placas,
                "no_economico": tractor.no_economico,
        }
        return data

    def get_data_cajas(self, Formulario):
        shipment = self.context['request'].GET.get('shipment')
        form = Formulario.__class__.objects.get(pk = shipment)
        cajas = Cajas.objects.get(id_formulario = form.pk)
        data =  {
                "linea_de_caja": cajas.linea_de_caja,
                "numero_caja": cajas.numero_caja,
                "placas": cajas.placas,
        }
        return data

    def get_data_ingreso(self, Formulario):
        shipment = self.context['request'].GET.get('shipment')
        form = Formulario.__class__.objects.get(pk = shipment)
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
        shipment = self.context['request'].GET.get('shipment')
        form = Formulario.__class__.objects.get(pk = shipment)
        checklist = CheckList.objects.get(id_formulario = form.pk)
        data = {
            
            "Tarjeta de circulación": checklist.DE_tarjeta_circulacion,
            "Seguro obligatorio": checklist.DE_seguro_obligatorio,
            "Placas físicas de circulación": checklist.DE_placas_fisicas,
            "Licencia federal": checklist.DE_licencia_federal,
            "Shiping, documentación de embarque": checklist.DS_doc_embarque,
            "Autorización de salida por embarques": checklist.DS_aut_embarque,
            "Detección K9": checklist.IN_det_k9,
            "Inclumpimiento CheckList": checklist.IN_incumplimiento_cl,
            "Estado inconveniente del transportista": checklist.IN_estado_inconveniente,
            "Entrada: Luces del frente": checklist.CGTE_luces_frente,
            "Entrada: Luces traseras": checklist.CGTE_luces_traseras,
            "Entrada: Motor": checklist.CGTE_motor,
            "Entrada: Tubo de escape": checklist.CGTE_tubo_escape,
            "Entrada: Exterior chasis": checklist.CGTE_exterior_chasis,
            "Entrada: Fugas de aceite": checklist.CGTE_fugas_aceite,
            "Entrada: Techo interior/exterior": checklist.CGTE_techo_int_ext,
            "Entrada: Puertas interiores/exteriores": checklist.CGTE_puertas_int_ext,
            "Entrada: Paredes laterales": checklist.CGTE_paredes_laterales,
            "Entrada: Parachoques": checklist.CGTE_parachoques,
            "Entrada: Piso": checklist.CGTE_piso,
            "Entrada: Patines": checklist.CGTE_patines,
            "Entrada: Quinta rueda": checklist.CGTE_quinta_rueda,
            "Entrada: Tanque de combustible": checklist.CGTE_tanque_combustible,
            "Entrada: Tanques de aire": checklist.CGTE_tanques_aire,
            "Entrada: Llantas y rines": checklist.CGTE_llantas_rines,
            "Entrada: Ejes": checklist.CGTE_ejes,
            "Entrada: Cabina": checklist.CGTE_cabina,
            "Entrada: Compartimiento herramientas": checklist.CGTE_comopartimientos_herramientas,
            "Entrada: Agrícolas (Plagas)": checklist.CGTE_agricolas,
            "Entrada: Olores extraños": checklist.CGTE_olores_ext,
            "Entrada: Humedad": checklist.CGTE_humedad,
            "Entrada: Objetos o sustancias extrañas": checklist.CGTE_obj_sust_ext,

            "Salida: Luces del frente": checklist.CGTS_luces_frente,
            "Salida: Luces traseras": checklist.CGTS_luces_traseras,
            "Salida: Motor": checklist.CGTS_motor,
            "Salida: Tubo de escape": checklist.CGTS_tubo_escape,
            "Salida: Exterior chasis": checklist.CGTS_exterior_chasis,
            "Salida: Fugas de aceite": checklist.CGTS_fugas_aceite,
            "Salida: Techo interior/exterior": checklist.CGTS_techo_int_ext,
            "Salida: Puertas interiores/exteriores": checklist.CGTS_puertas_int_ext,
            "Salida: Paredes laterales": checklist.CGTS_paredes_laterales,
            "Salida: Parachoques": checklist.CGTS_parachoques,
            "Salida: Piso": checklist.CGTS_piso,
            "Salida: Patines": checklist.CGTS_patines,
            "Salida: Quinta rueda": checklist.CGTS_quinta_rueda,
            "Salida: Tanque de combustible": checklist.CGTS_tanque_combustible,
            "Salida: Tanques de aire": checklist.CGTS_tanques_aire,
            "Salida: Llantas y rines": checklist.CGTS_llantas_rines,
            "Salida: Ejes": checklist.CGTS_ejes,
            "Salida: Cabina": checklist.CGTS_cabina,
            "Salida: Compartimiento herramientas": checklist.CGTS_comopartimientos_herramientas,
            "Salida: Agrícolas (Plagas)": checklist.CGTS_agricolas,
            "Salida: Olores extraños": checklist.CGTS_olores_ext,
            "Salida: Humedad": checklist.CGTS_humedad,
            "Salida: Objetos o sustancias extrañas": checklist.CGTS_obj_sust_ext,

        }
        return data

    def get_data_revision_canina(self, Formulario):
        shipment = self.context['request'].GET.get('shipment')
        form = Formulario.__class__.objects.get(pk = shipment)
        revision_can = RevisionCanina.objects.get(id_formulario = form.pk)
        data =  {
            "Patio": revision_can.patio,
            "Cliente": revision_can.cliente,
            "Nombre del K9": revision_can.nombre_k9,
            "Defensa": revision_can.PR_defensa,
            "Motor": revision_can.PR_motor,
            "Piso de cabina": revision_can.PR_piso_cabina,
            "Tanque de Combustible": revision_can.PR_tanque_combustible,
            "Llantas y Rines": revision_can.PR_llantas_rines,
            "Flecha": revision_can.PR_flecha,
            "Cabina": revision_can.PR_cabina,
            "Tanque de aire": revision_can.PR_tanque_aire,
            "Mofles/Escape": revision_can.PR_mofles,
            "Equipo de refigeración": revision_can.PR_equipo_refrigeracion,
            "Quinta Rueda": revision_can.PR_quinta_rueda,
            "Chasis": revision_can.PR_chasis,
            "Puertas traseras": revision_can.PR_puertas_traseras,
            "Paredes/Techo": revision_can.PR_paredes_techo,
            "Piso de la caja": revision_can.PR_piso_caja,
            #"descripcion_hallazgo": revision_can.descripcion_hallazgo,
        }
        return data
from django.db import models

from authentication.models import CustomUser

# Create your models here.

class Guardia(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return f"ID: {self.id} - Guardia: {self.user}"

class Linea(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f"{self.name}"

class Destino(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"Destino: {self.name}"

class ContactoClave(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)

    def get_full_name_user(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"Contacto Clave: {self.first_name} {self.last_name}"

class Embarque(models.Model):
    creado_por = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    guardia = models.ForeignKey(Guardia, on_delete=models.DO_NOTHING)
    operador = models.CharField(max_length=50, blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    linea_transporte = models.ForeignKey(Linea, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="linea_transporte")
    marca_tractor = models.CharField(max_length=50, blank=True, null=True)
    numero_placas_tractor = models.CharField(max_length=50, blank=True, null=True)
    no_economico = models.CharField(max_length=30, blank=True, null=True)

    linea_de_caja = models.ForeignKey(Linea, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="linea_de_caja")
    numero_caja = models.CharField(max_length=40, blank=True, null=True)
    numero_placas_caja = models.CharField(max_length=30, blank=True, null=True)

    autorizado_por = models.ForeignKey(ContactoClave, blank=True, null=True, on_delete=models.DO_NOTHING)
    factura = models.CharField(max_length=80, blank=True, null=True)
    numero_pallets = models.CharField(max_length=30, blank=True, null=True)
    #numero_sello = models.CharField(max_length=30, blank=True, null=True)
    #sello_entregado_a = models.CharField(max_length=50, blank=True, null=True)
    destino = models.ForeignKey(Destino, on_delete=models.DO_NOTHING, blank=True, null=True)
    es_exportacion = models.BooleanField(blank=True, null=True)
    def __str__(self):
        return f"{self.pk} - Creado por: {self.creado_por} - Guardia: {self.guardia}"
    
    @property
    def linea_name(self):
        return self.linea_transporte.name

    @property
    def destino_name(self):
        return self.destino.name

    @property
    def autorizado_por_full_name(self):
        return self.autorizado_por.get_full_name_user()


# class Formulario(models.Model):
#     # TODO Fecha y hora de llegada Formato 24 HRS
#     # TODO Fecha y hora de Entrada y de Salida Formato 24 HRS
#     creado_por = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
#     guardia = models.CharField(max_length=50, blank=True, null=True)
#     operador = models.CharField(max_length=50, blank=True, null=True)

#     creado = models.DateTimeField(auto_now_add=True)
#     modificado = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.pk} - Creado por: {self.creado_por} - Guardia: {self.guardia}"

# class Tractor(models.Model):
#     id_formulario = models.ForeignKey(Formulario, on_delete=models.DO_NOTHING)
#     linea_transporte = models.CharField(max_length=50, blank=True, null=True)
#     marca_tractor = models.CharField(max_length=50, blank=True, null=True)
#     numero_placas = models.CharField(max_length=50, blank=True, null=True)
#     no_economico = models.CharField(max_length=30, blank=True, null=True)

# class Cajas(models.Model):
#     id_formulario = models.ForeignKey(Formulario, on_delete=models.DO_NOTHING)
#     linea_de_caja = models.CharField(max_length=40, blank=True, null=True)
#     numero_caja = models.CharField(max_length=40, blank=True, null=True)
#     placas = models.CharField(max_length=30, blank=True, null=True)

# class Ingreso(models.Model):
#     id_formulario = models.ForeignKey(Formulario, on_delete=models.DO_NOTHING)
#     autorizado_por = models.CharField(max_length=80, blank=True, null=True)
#     factura = models.CharField(max_length=80, blank=True, null=True)
#     numero_pallets = models.CharField(max_length=30, blank=True, null=True)
#     numero_sello = models.CharField(max_length=30, blank=True, null=True)
#     sello_entregado_a = models.CharField(max_length=50, blank=True, null=True)
#     destino = models.CharField(max_length=50, blank=True, null=True)
#     es_exportacion = models.BooleanField(blank=True, null=True)

class Entrada(models.Model):
    embarque_id = models.ForeignKey(Embarque, on_delete=models.DO_NOTHING)
    numero_cajas_embarque = models.CharField(max_length=40, blank=True, null=True)
    DE_tarjeta_circulacion = models.BooleanField(blank=True, null=True)
    DE_seguro_obligatorio = models.BooleanField(blank=True, null=True)
    DE_placas_fisicas = models.BooleanField(blank=True, null=True)
    DE_licencia_federal = models.BooleanField(blank=True, null=True)

    # IN_det_k9 = models.BooleanField(blank=True, null=True)
    # IN_incumplimiento_cl = models.BooleanField(blank=True, null=True)
    # IN_estado_inconveniente = models.BooleanField(blank=True, null=True)
    CGTE_luces_frente = models.BooleanField(blank=True, null=True)
    CGTE_luces_traseras = models.BooleanField(blank=True, null=True)
    CGTE_motor = models.BooleanField(blank=True, null=True)
    CGTE_tubo_escape = models.BooleanField(blank=True, null=True)
    CGTE_exterior_chasis = models.BooleanField(blank=True, null=True)
    CGTE_fugas_aceite = models.BooleanField(blank=True, null=True)
    CGTE_techo_int_ext = models.BooleanField(blank=True, null=True)
    CGTE_puertas_int_ext = models.BooleanField(blank=True, null=True)
    CGTE_paredes_laterales = models.BooleanField(blank=True, null=True)
    CGTE_parachoques = models.BooleanField(blank=True, null=True)
    CGTE_piso = models.BooleanField(blank=True, null=True)
    CGTE_patines = models.BooleanField(blank=True, null=True)
    CGTE_quinta_rueda = models.BooleanField(blank=True, null=True)
    CGTE_tanque_combustible = models.BooleanField(blank=True, null=True)
    CGTE_tanques_aire = models.BooleanField(blank=True, null=True)
    CGTE_llantas_rines = models.BooleanField(blank=True, null=True)
    CGTE_ejes = models.BooleanField(blank=True, null=True)
    CGTE_cabina = models.BooleanField(blank=True, null=True)
    CGTE_comopartimientos_herramientas = models.BooleanField(blank=True, null=True)
    CGTE_agricolas = models.BooleanField(blank=True, null=True)
    CGTE_olores_ext = models.BooleanField(blank=True, null=True)
    CGTE_humedad = models.BooleanField(blank=True, null=True)
    CGTE_obj_sust_ext = models.BooleanField(blank=True, null=True)

    comentarios_entrada = models.CharField(max_length=50, blank=True, null=True)
    guardia_entrada = models.ForeignKey(Guardia, on_delete=models.DO_NOTHING)

class Salida(models.Model):
    embarque_id = models.ForeignKey(Embarque, on_delete=models.DO_NOTHING)
    DS_doc_embarque = models.BooleanField(blank=True, null=True)
    DS_aut_embarque = models.BooleanField(blank=True, null=True)
    DS_has_sello = models.BooleanField(blank=True, null=True)
    DS_sello = models.CharField(max_length=40, blank=True, null=True)

    CGTS_luces_frente = models.BooleanField(blank=True, null=True)
    CGTS_luces_traseras = models.BooleanField(blank=True, null=True)
    CGTS_motor = models.BooleanField(blank=True, null=True)
    CGTS_tubo_escape = models.BooleanField(blank=True, null=True)
    CGTS_exterior_chasis = models.BooleanField(blank=True, null=True)
    CGTS_fugas_aceite = models.BooleanField(blank=True, null=True)
    CGTS_techo_int_ext = models.BooleanField(blank=True, null=True)
    CGTS_puertas_int_ext = models.BooleanField(blank=True, null=True)
    CGTS_paredes_laterales = models.BooleanField(blank=True, null=True)
    CGTS_parachoques = models.BooleanField(blank=True, null=True)
    CGTS_piso = models.BooleanField(blank=True, null=True)
    CGTS_patines = models.BooleanField(blank=True, null=True)
    CGTS_quinta_rueda = models.BooleanField(blank=True, null=True)
    CGTS_tanque_combustible = models.BooleanField(blank=True, null=True)
    CGTS_tanques_aire = models.BooleanField(blank=True, null=True)
    CGTS_llantas_rines = models.BooleanField(blank=True, null=True)
    CGTS_ejes = models.BooleanField(blank=True, null=True)
    CGTS_cabina = models.BooleanField(blank=True, null=True)
    CGTS_comopartimientos_herramientas = models.BooleanField(blank=True, null=True)
    CGTS_agricolas = models.BooleanField(blank=True, null=True)
    CGTS_olores_ext = models.BooleanField(blank=True, null=True)
    CGTS_humedad = models.BooleanField(blank=True, null=True)
    CGTS_obj_sust_ext = models.BooleanField(blank=True, null=True)

    comentarios_salida = models.CharField(max_length=50, blank=True, null=True)
    guardia_salida = models.ForeignKey(Guardia, on_delete=models.DO_NOTHING)


# class CheckList(models.Model):
#     """
#         Modelo para almacenar el documento CheckList

#         Nomenclatura especial:
        
#         DE = Documento de Entrada
#         DS = Documento de salida
#         IN = Incidencias
#         CGTE = Condiciones generales del transporte entrada
#         CGTS = Condiciones generales del transporte salida
#     """

#     id_formulario = models.ForeignKey(Formulario, on_delete=models.DO_NOTHING)
#     numero_cajas_embarque = models.CharField(max_length=40, blank=True, null=True)
#     DE_tarjeta_circulacion = models.BooleanField(blank=True, null=True)
#     DE_seguro_obligatorio = models.BooleanField(blank=True, null=True)
#     DE_placas_fisicas = models.BooleanField(blank=True, null=True)
#     DE_licencia_federal = models.BooleanField(blank=True, null=True)

#     DS_doc_embarque = models.BooleanField(blank=True, null=True)
#     DS_aut_embarque = models.BooleanField(blank=True, null=True)
#     DS_sello = models.CharField(max_length=40, blank=True, null=True)

#     IN_det_k9 = models.BooleanField(blank=True, null=True)
#     IN_incumplimiento_cl = models.BooleanField(blank=True, null=True)
#     IN_estado_inconveniente = models.BooleanField(blank=True, null=True)
#     CGTE_luces_frente = models.BooleanField(blank=True, null=True)
#     CGTE_luces_traseras = models.BooleanField(blank=True, null=True)
#     CGTE_motor = models.BooleanField(blank=True, null=True)
#     CGTE_tubo_escape = models.BooleanField(blank=True, null=True)
#     CGTE_exterior_chasis = models.BooleanField(blank=True, null=True)
#     CGTE_fugas_aceite = models.BooleanField(blank=True, null=True)
#     CGTE_techo_int_ext = models.BooleanField(blank=True, null=True)
#     CGTE_puertas_int_ext = models.BooleanField(blank=True, null=True)
#     CGTE_paredes_laterales = models.BooleanField(blank=True, null=True)
#     CGTE_parachoques = models.BooleanField(blank=True, null=True)
#     CGTE_piso = models.BooleanField(blank=True, null=True)
#     CGTE_patines = models.BooleanField(blank=True, null=True)
#     CGTE_quinta_rueda = models.BooleanField(blank=True, null=True)
#     CGTE_tanque_combustible = models.BooleanField(blank=True, null=True)
#     CGTE_tanques_aire = models.BooleanField(blank=True, null=True)
#     CGTE_llantas_rines = models.BooleanField(blank=True, null=True)
#     CGTE_ejes = models.BooleanField(blank=True, null=True)
#     CGTE_cabina = models.BooleanField(blank=True, null=True)
#     CGTE_comopartimientos_herramientas = models.BooleanField(blank=True, null=True)
#     CGTE_agricolas = models.BooleanField(blank=True, null=True)
#     CGTE_olores_ext = models.BooleanField(blank=True, null=True)
#     CGTE_humedad = models.BooleanField(blank=True, null=True)
#     CGTE_obj_sust_ext = models.BooleanField(blank=True, null=True)

#     CGTS_luces_frente = models.BooleanField(blank=True, null=True)
#     CGTS_luces_traseras = models.BooleanField(blank=True, null=True)
#     CGTS_motor = models.BooleanField(blank=True, null=True)
#     CGTS_tubo_escape = models.BooleanField(blank=True, null=True)
#     CGTS_exterior_chasis = models.BooleanField(blank=True, null=True)
#     CGTS_fugas_aceite = models.BooleanField(blank=True, null=True)
#     CGTS_techo_int_ext = models.BooleanField(blank=True, null=True)
#     CGTS_puertas_int_ext = models.BooleanField(blank=True, null=True)
#     CGTS_paredes_laterales = models.BooleanField(blank=True, null=True)
#     CGTS_parachoques = models.BooleanField(blank=True, null=True)
#     CGTS_piso = models.BooleanField(blank=True, null=True)
#     CGTS_patines = models.BooleanField(blank=True, null=True)
#     CGTS_quinta_rueda = models.BooleanField(blank=True, null=True)
#     CGTS_tanque_combustible = models.BooleanField(blank=True, null=True)
#     CGTS_tanques_aire = models.BooleanField(blank=True, null=True)
#     CGTS_llantas_rines = models.BooleanField(blank=True, null=True)
#     CGTS_ejes = models.BooleanField(blank=True, null=True)
#     CGTS_cabina = models.BooleanField(blank=True, null=True)
#     CGTS_comopartimientos_herramientas = models.BooleanField(blank=True, null=True)
#     CGTS_agricolas = models.BooleanField(blank=True, null=True)
#     CGTS_olores_ext = models.BooleanField(blank=True, null=True)
#     CGTS_humedad = models.BooleanField(blank=True, null=True)
#     CGTS_obj_sust_ext = models.BooleanField(blank=True, null=True)

#     comentarios = models.CharField(max_length=50, blank=True, null=True)
#     guardia_entrada = models.CharField(max_length=50, blank=True, null=True)
#     guardia_salida = models.CharField(max_length=50, blank=True, null=True)

class RevisionCanina(models.Model):
    """
        Nomenclatura

        PR = Puntos de revisión
    """
    embarque_id = models.ForeignKey(Embarque, on_delete=models.DO_NOTHING)
    # TODO Hora de revisión canina
    patio = models.CharField(max_length=40, blank=True, null=True)
    cliente = models.CharField(max_length=40, blank=True, null=True)
    nombre_k9 = models.CharField(max_length=50, blank=True, null=True)

    PR_defensa = models.BooleanField(blank=True, null=True)
    PR_motor = models.BooleanField(blank=True, null=True)
    PR_piso_cabina = models.BooleanField(blank=True, null=True)
    PR_tanque_combustible = models.BooleanField(blank=True, null=True)
    PR_llantas_rines = models.BooleanField(blank=True, null=True)
    PR_flecha = models.BooleanField(blank=True, null=True)
    PR_cabina = models.BooleanField(blank=True, null=True)
    PR_tanque_aire = models.BooleanField(blank=True, null=True)
    PR_mofles = models.BooleanField(blank=True, null=True)
    PR_equipo_refrigeracion = models.CharField(max_length = 10, blank=True, null=True)
    PR_quinta_rueda = models.BooleanField(blank=True, null=True)
    PR_chasis = models.BooleanField(blank=True, null=True)
    PR_puertas_traseras = models.BooleanField(blank=True, null=True)
    PR_paredes_techo = models.BooleanField(blank=True, null=True)
    PR_piso_caja = models.BooleanField(blank=True, null=True)
    descripcion_hallazgo = models.CharField(max_length = 1000, blank=True, null=True)

    #TODO Nombre y firma del manejador
    #TODO Nombre y firma del operador

class Feedback(models.Model):
    # Modelo para manejar feedback recopilado de la app
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    descripcion = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
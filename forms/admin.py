from django.contrib import admin
from .models import Formulario, Tractor, Cajas, Ingreso, CheckList, RevisionCanina

# Register your models here.
admin.site.register(Formulario)
admin.site.register(Tractor)
admin.site.register(Cajas)
admin.site.register(Ingreso)
admin.site.register(CheckList)
admin.site.register(RevisionCanina)


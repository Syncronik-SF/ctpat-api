from django.contrib import admin

from forms.models import Embarque, Entrada, Feedback, Guardia, RevisionCanina, Salida
#from .models import Formulario, Tractor, Cajas, Ingreso, CheckList, RevisionCanina, Feedback

# Register your models here.
admin.site.register(Guardia)
admin.site.register(Embarque)
admin.site.register(Entrada)
admin.site.register(Salida)
admin.site.register(RevisionCanina)

admin.site.register(Feedback)
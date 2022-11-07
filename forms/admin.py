from django.contrib import admin

from forms.models import Embarque, Entrada, Feedback, Guardia, RevisionCanina, Salida, Linea, Destino, ContactoClave
#from .models import Formulario, Tractor, Cajas, Ingreso, CheckList, RevisionCanina, Feedback

# Register your models here.
admin.site.register(Guardia)
admin.site.register(Embarque)
admin.site.register(Entrada)
admin.site.register(Salida)
admin.site.register(RevisionCanina)
admin.site.register(Linea)
admin.site.register(Destino)
admin.site.register(ContactoClave)

admin.site.register(Feedback)
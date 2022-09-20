from django.contrib import admin
from .models import Incidence

# Register your models here.


@admin.register(Incidence)
class IncidenceAdmin(admin.ModelAdmin):
    ordering=('id',)    
    list_display=('date','id','title','descripcion',)
    search_fields= ('id','title','date',)
    list_editable=('title',)
    list_display_links=('id',)
    list_filter=('user',)
    list_per_page=5
    exclude=('incidencias',)

#admin.site.register(Incidence)


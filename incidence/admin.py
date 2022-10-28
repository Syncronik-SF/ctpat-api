from django.contrib import admin
from .models import Incidence, IncidenceType

# Register your models here.


@admin.register(Incidence)
class IncidenceAdmin(admin.ModelAdmin):
    ordering=('id',)    
    list_display=('date','id','incidence_type', 'origen', 'descripcion',)
    search_fields= ('id','incidence_type','date',)
    list_editable=('incidence_type',)
    list_display_links=('id',)
    list_filter=('user',)
    list_per_page=5
    exclude=('incidencias',)


@admin.register(IncidenceType)
class IncidenceTypeAdmin(admin.ModelAdmin):
    list_display=('id','type')


#admin.site.register(Incidence)


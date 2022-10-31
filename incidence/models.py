from io import open_code
from django.db import models
from authentication.models import CustomUser
from forms.models import Embarque
#from forms.models import RevisionCanina, CheckList
from django.core.validators import FileExtensionValidator


class IncidenceType(models.Model):
    type = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return f"ID: {self.id} - Tipo: {self.type}"


class Incidence(models.Model):
    '''Model for get the register of incidence'''
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    embarque = models.ForeignKey(Embarque, on_delete=models.DO_NOTHING, null=True)
    incidence_type = models.ForeignKey(IncidenceType, on_delete=models.DO_NOTHING, null=True)
    origen = models.CharField(max_length=100, default="")
    descripcion = models.TextField(default="",null=True, blank=True)
    date = models.DateField( auto_now_add=True, null=True, blank=True)
    hour = models.TimeField(auto_now_add=True)
    picture = models.ImageField(upload_to="incidence"  ,blank=True, null=True)

    def __str__(self):
        return f" {self.id}: {self.incidence_type}"
    

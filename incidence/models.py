from django.db import models
from authentication.models import CustomUser
from forms.models import RevisionCanina, CheckList
from django.core.validators import FileExtensionValidator




class Incidence(models.Model):
    '''Model for get the register of incidence'''
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    
    title= models.CharField(max_length=50)
    descripcion = models.TextField(default="",null=True, blank=True)
    date = models.DateField( auto_now_add=True, null=True, blank=True)
    hour = models.TimeField(auto_now_add=True)
    picture = models.ImageField(upload_to="incidence"  ,blank=True, null=True)

    def __str__(self):
        return f" {self.id}: {self.title}"
    

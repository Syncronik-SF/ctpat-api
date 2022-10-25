from django.db import models
from django.utils import timezone

class InOut(models.Model):
    option = models.CharField(max_length=10)

    def __str__(self):
        return f"ID: {self.id} - Option: {self.option}"
    

class RegisterInOut(models.Model):
    option = models.ForeignKey(InOut, on_delete=models.DO_NOTHING)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=15)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"ID: {self.id} - Full Name: {self.full_name} - Phone: {self.phone} - Date: {self.date} - Hour: {self.time}"

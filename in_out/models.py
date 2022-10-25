from django.db import models
from django.utils import timezone

class RegisterInOut(models.Model):
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=15)
    dt_in = models.DateTimeField(default=timezone.now)
    dt_out = models.DateTimeField(null=True)
    
    def __str__(self) -> str:
        return f"ID: {self.id} - Full Name: {self.full_name} - Phone: {self.phone} - Date Time In: {self.dt_in} - Date Time Out: {self.dt_out}"

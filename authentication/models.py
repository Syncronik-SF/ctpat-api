from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import DO_NOTHING

def nameFile(instance, filename):
    return '/'.join(['images', str(instance.name), filename])

class WorkerType(models.Model):
    worker_type = models.CharField(max_length=50)
    def __str__(self) -> str:
        return f"ID: {self.id} - Type: {self.worker_type}"

class CustomUser(AbstractUser):
    """
        Profile user model
    """
    email = models.EmailField(max_length=150, unique=False)
    phone = models.CharField(max_length=120, blank=True)
    job_title = models.CharField(max_length=40, null=True, blank=True)
    is_online_in_app = models.BooleanField(default=False, null=True)
    worker_type = models.ForeignKey(WorkerType, null=True, blank=True, on_delete=models.DO_NOTHING)    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def get_full_name_user(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_username(self):
        return self.username

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user_profile', on_delete=models.CASCADE)
    profile_picture = models.ImageField(max_length=300,upload_to='profile_pics', 
            blank=True, 
            null=True, default="profile_pics/user.png")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    


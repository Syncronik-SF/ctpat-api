from django.urls import path
from .views import RegisterInOutAPI

urlpatterns = [
    path('register', RegisterInOutAPI.as_view()),
]
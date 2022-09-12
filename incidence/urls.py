from incidence import views
from django.urls import path
from .views import incidence_post




urlpatterns = [
    path('', views.incidence_post)
 ] #Crea incidence

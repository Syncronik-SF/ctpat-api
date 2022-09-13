from incidence import views
from django.urls import path
from .views import *




urlpatterns = [
    path('create/', views.incidence_post),
    path('update/<pk>',views.incidence_update),
    path('delete/<pk>',views.incidence_delete),
    



 ] #Crea incidence

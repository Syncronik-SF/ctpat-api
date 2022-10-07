from incidence import views
from django.urls import path
from .views import *




urlpatterns = [
    path('create/', views.incidence_post),
    path('update/<pk>',views.incidence_update),
    path('delete/<pk>',views.incidence_delete),
    path('detail-incidence/<pk>', views.incidence_detail),
    path('detail', Datelist.as_view(), name= "detail_date"),
    path('all', AllIncidence.as_view(), name= "all_incidence"),
    



 ] #Crea incidence

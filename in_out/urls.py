from django.urls import path
from .views import ListAllRegister, ListRegisterByDate, ListRegisterWithoutOut, RegisterInAPI, RegisterOutAPI

urlpatterns = [
    path('register-in', RegisterInAPI.as_view()),
    path('all', ListAllRegister.as_view()),
    path('list', ListRegisterByDate.as_view()),
    path('list-without-out', ListRegisterWithoutOut.as_view()),
    path('register-out/<int:register_id>/', RegisterOutAPI.as_view()),
]
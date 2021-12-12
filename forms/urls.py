from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CreateForm, GetForms, ping, GetFormDetails

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    # Forms views
    path("ping", ping, name="pong"),
    path("create-form", CreateForm.as_view(), name="create-form"),
    path("forms/all", GetForms.as_view({'get': 'list'}), name="get-forms"),
    path("forms/details", GetFormDetails.as_view({'get': 'list'}), name="get-forms-details"),
]
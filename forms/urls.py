from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CreateForm, GetForms, GetLastFiveForms, SaveFeedback, ping, GetFormDetails

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    # Forms views
    path("ping", ping, name="pong"),
    path("create-form", CreateForm.as_view(), name="create-form"),
    path("forms/all", GetForms.as_view({'get': 'list'}), name="get-forms"),
    path("forms/details", GetFormDetails.as_view({'get': 'list'}), name="get-forms-details"),
    path("forms/last-five", GetLastFiveForms.as_view({'get': 'list'}), name="get-last-five"),
    path("feedback/save", SaveFeedback.as_view(), name="save-feedback")
]
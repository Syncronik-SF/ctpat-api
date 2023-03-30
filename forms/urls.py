from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CreateEmbarque, CreateEntrada, CreateRevisionCan, CreateSalida, GetFormDetails, GetForms, GetLastFiveForms, ListGuardias, Quantities, SaveFeedback, forms_created, ping, validate_status_form, ListLineas, ListDestinos, ListContactosClave, ViewPDF, RenderPDFView
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    # Forms views
    path("ping", ping, name="pong"),
    path("create-embarque", CreateEmbarque.as_view(), name="create-form"),
    path("create-entrada", CreateEntrada.as_view(), name="create-entrada"),
    path("create-canina", CreateRevisionCan.as_view(), name="create-canina"),
    path("create-salida", CreateSalida.as_view(), name="create-salida"),
    path("forms/all", GetForms.as_view({'get': 'list'}), name="get-forms"),
    path("forms/details", GetFormDetails.as_view({'get': 'list'}), name="get-forms-details"),
    path("forms/last-five", GetLastFiveForms.as_view({'get': 'list'}), name="get-last-five"),
    path("feedback/save", SaveFeedback.as_view(), name="save-feedback"),
    path("guardias/all", ListGuardias.as_view()),
    path('lineas/all', ListLineas.as_view()),
    path('contactos/all', ListContactosClave.as_view()),
    path('destinos/all', ListDestinos.as_view()),
    path('forms-pending/<pk>', forms_created),
    path('status/<pk>', validate_status_form),
    
    path('quantities/<str:date>/', Quantities.as_view()),
    path('generate_pdf/', ViewPDF.as_view(), name="pdf_view"),
    path('pdf_view/', RenderPDFView.as_view(), name="render_pdf")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
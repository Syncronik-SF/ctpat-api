from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Api routes
    path('api/v1/', include('authentication.urls')),
    path('api/v1/', include(('forms.urls', 'forms'))),
    path('api/v1/generate_token/', views.obtain_auth_token),
    path('api/v1/incidence/', include('incidence.urls')),
    path('api/v1/in-out/', include('in_out.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
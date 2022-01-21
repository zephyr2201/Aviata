from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path("api/prov_bastian/", include("prov_bastian.urls")),
    path("api/prov_arystan/", include("prov_arystan.urls")),
    path("api/airflow/", include("airflow.urls"), name='airlfow'),
]

from django.urls import include, path
from . import views


urlpatterns = [
    path("search/", views.ProvArystanViewSet.as_view({'get': 'search'}), name='arystan'),
]

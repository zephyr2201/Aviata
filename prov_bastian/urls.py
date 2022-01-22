from django.urls import path
from . import views


urlpatterns = [
    path("search/", views.ProvBastianViewSet.as_view({'get': 'search'}), name='bastian'),
]

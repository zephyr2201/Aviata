from django.urls import include, path
from . import views


urlpatterns = [
    path("search/", views.AirFlowViewSet.as_view({'get': 'search'})),
    path("results/<str:search_id>/<str:currency>/", views.AirFlowViewSet.as_view({'get': 'results'}), name='search_results'),

]

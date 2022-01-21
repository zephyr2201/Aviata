from typing import Type

from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.status import HTTP_200_OK

from prov_arystan.services import get_flights
from prov_bastian.serializers import ResultReadSerializer


class ProvArystanViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet):

    def get_serializer_class(self) -> Type[BaseSerializer]:
        actions = {
            'search': ResultReadSerializer,
        }
        return actions[self.action]

    def search(self, request: Request) -> Response:
        data = get_flights()
        return Response(data, HTTP_200_OK)

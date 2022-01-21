from unittest import result
from uuid import uuid4
from celery import group

from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from airflow.tasks import provider_search_task

from airflow.utils import create_search_id, prepare_response_data


class AirFlowViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):

    def search(self, request: Request, pk=None) -> Response:
        search_id = uuid4()
        provider_search_task.check_course()
        create_search_id(search_id)
        group(
            provider_search_task.si(search_id, 1),
            provider_search_task.si(search_id, 2),
        ).apply_async()
        return Response({"search_id": str(search_id)}, HTTP_200_OK)
    
    def results(self, request: Request, search_id=None, currency=None) -> Response:
        data = prepare_response_data(search_id, currency)
        return Response(data, HTTP_200_OK)

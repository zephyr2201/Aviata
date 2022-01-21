import uuid
import requests
from urllib.error import HTTPError

from django.urls import reverse

from airflow.models import Provider, SearchResult
from airflow.services import ModelBasedService
from airflow.services.serializers import SearchResultReadSerializer


class ProviderSearchService(ModelBasedService):

    read_serializer = SearchResultReadSerializer
    host = 'http://web:9000'
    link: str = ''
    serach_id : uuid.uuid4 = ''
    instance_model = Provider

    def __init__(self, search_id, code: int):
        self.instance_code = code
        self.link = reverse('arystan')
        if code == 2:
            self.link = reverse('bastian')
        self.serach_id = search_id        

    def create_search_result(self):
        search_result = SearchResult.objects.create(provider=self.instance, search_id=self.serach_id)
        return search_result

    def make_request(self, **kwargs):
        search_result = self.create_search_result()
        response = requests.get(
            url=self.host+self.link,
        )
        if response.ok:
            return self.finalize_response(self.prepare_response_data(response), search_result)
        elif response.status_code == 400:
            return self.handle_400_exception(response)
        elif response.status_code == 404:
            raise self.handle_400_exception(response)
        elif response.status_code == 500:
            return self.handle_500_exception(response)
        raise HTTPError(response.text)

    def prepare_response_data(self, response):
        try:
            return {'data': response.json()}
        except:
            return {}

    def finalize_response(self, prepared_data: dict, search_result: SearchResult) -> dict:
        if not prepared_data:
            return {'error': 'Failed'}
        serializer = self.read_serializer(instance=search_result, data=prepared_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        search_result.completed()
        search_result.save()
        return serializer.data

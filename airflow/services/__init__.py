import requests
from abc import ABC
from urllib.parse import urljoin
from requests.exceptions import InvalidURL, HTTPError

from django.core.exceptions import ObjectDoesNotExist


class BaseService(object):
    endpoint: str = ''
    instance_pk: int = 0
    timeout: int = 20
    headers: dict = {}

    @property
    def host(self):
        raise NotImplementedError

    @property
    def code(self):
        raise NotImplementedError

    @property
    def url(self):
        return urljoin(self.host, self.endpoint)

    def prepare_request_data(self, **kwargs):
        return {'json': kwargs}

    def prepare_response_data(self, response):
        try:
            return response.json()
        except:
            return {}

    def make_request(self, **kwargs):
        response = requests.post(
            url=self.host + self.endpoint,
            headers=self.headers,
            timeout=self.timeout,
            **self.prepare_request_data(**kwargs)
        )

        if response.ok:
            print ('response goes here', response)
            return self.finalize_response(self.prepare_response_data(response))
        elif response.status_code == 400:
            return self.handle_400_exception(response)
        elif response.status_code == 404:
            raise InvalidURL(self.url)
        elif response.status_code == 500:
            return self.handle_500_exception(response)

        raise HTTPError(response.text)

    def finalize_response(self, prepared_response):
        return prepared_response

    def handle_400_exception(self, response):
        return response.text

    def handle_500_exception(self, response):
        raise HTTPError(response.text)

    def __call__(self, **kwargs):
        return self.make_request(**kwargs)


class ModelBasedService(BaseService, ABC):
    cache_expiration = 10
    cache_used = False

    @property
    def instance_model(self):
        raise NotImplementedError

    @property
    def instance(self):
        try:
            return self.instance_model.objects.get(id=self.instance_code)
        except ObjectDoesNotExist as e:
            raise e

    def __init__(self, instance_code: str):
        self.instance_code = instance_code

    @property
    def response_serializer(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        resp = self.make_request(**kwargs)
        return resp

    def finalize_response(self, prepared_response):
        serializer = self.response_serializer(instance=self.instance, data=prepared_response)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data

import requests
from uuid import uuid4
from bs4 import BeautifulSoup
from urllib.error import HTTPError

from celery import Task
from core.celery_app import app

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from airflow.models import Currency, UUIDModel
from airflow.services.integrations import ProviderSearchService


class TaskFailed(ValidationError):
    default_detail = "Задача не успешна."


class ProviderSearchTask(Task):

    #Проверить курс для старта
    @staticmethod
    def check_course():
        if not Currency.objects.last():
            request_for_currency()

    def failed(self, error):
        raise TaskFailed
    
    def success(self):
        pass

    def run(self, search_id: uuid4, pk: int):
        obj = UUIDModel.objects.get(uuid=search_id)

        self.service = ProviderSearchService(obj, pk)
        response = self.service()

        if response and (error := response.get('error', '')):
            self.failed(error)


@app.task(max_retries=None, time_limit=10800)
def request_for_currency() -> None: # Request to request the exchange rate
    time = timezone.now()
    params = {
        'fdate': time.strftime("%d.%m.%Y")
    }
    url = 'https://www.nationalbank.kz/rss/get_rates.cfm'
    response = requests.get(url, params=params)
    if response.ok:
        return prepare_currency_data(response)
    raise HTTPError(response.text)


@app.task(max_retries=None, time_limit=10800)
def prepare_currency_data(response: Response) -> None: # Parse data
    data = {}
    text = response.text
    xml_text = text.encode()

    soup = BeautifulSoup(xml_text, 'xml')
    items = soup.find_all('item')
    for item in items:
        title = item.find('title').text
        price = item.find('description').text
        data[title] = price

    Currency.objects.create(data=data)


provider_search_task = app.register_task(ProviderSearchTask())

import json
from typing import Dict, List

from airflow import ProvaiderSearchStatus
from airflow.models import Currency, SearchResult, UUIDModel


def create_search_id(search_id) -> UUIDModel:
    obj = UUIDModel.objects.create(uuid=search_id)
    return obj


def prepare_response_data(search_id: str, currency) -> Dict: # Results data
    results = get_provider_serach_results(search_id)

    data = {
        'search_id': search_id,
        'status': results.get('status'),
        'items': results.get('data')
    }

    if not results.get('data'):
        return data

    supplemented_data = currency_translation(currency, results.get('data'))
    data['items'] = sorted(supplemented_data, key=lambda d: float(d.get('price')), reverse=True)

    return data


def get_provider_serach_results(search_id: str) -> Dict:
    count = 0
    results = []
    search_results = SearchResult.objects.filter(search_id__uuid=search_id)

    for result in search_results:
        if result.status == ProvaiderSearchStatus.PENDING:
            count += 1
            continue

        results.extend(json.loads(result.data))

    return {
        'data': results,
        'status': 'PENDING' if count >=1 else 'COMPLETED'
    }


def currency_translation(currency: str, results: List) -> List:
    obj = Currency.objects.last()
    data = obj.data
    for result in results:
        cur = result.get('pricing').get('currency')
        total = result.get('pricing').get('total')
        if cur == currency:
            result['price'] = {
                    'amount': float(total),
                    'currency': currency
                    }
            continue

        if currency == 'KZT':
            price = data.get(cur)
            result['price'] = {'amount': float(total) * float(price), 'currency': currency}
            continue

        price = data.get(currency)
        if cur == 'KZT':
            result['price'] = {'amount': float(total) / float(price), 'currency': currency}
            continue

        result['price'] = {'amount': float(cur), 'currency': currency}
    return results

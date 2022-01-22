import json
import time
from typing import Dict


def get_flights() -> str:
    with open('prov_arystan/response_a.json', 'r') as f:
        data = f.read()
    time.sleep(30)
    return data

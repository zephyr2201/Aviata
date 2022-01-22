import json
import time
from typing import Dict


def get_flights() -> str:
    with open('prov_bastian/response_b.json', 'r') as f:
        data = f.read()
    time.sleep(60)
    return data

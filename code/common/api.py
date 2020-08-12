import os
import json
import uuid

from datetime import datetime
from .config import endpoints


class Api():

    def __init__(self, region):
        self.region = region

    def get(self, client, userId, name="Get balance"):
        endpoint = endpoints[self.region]['get']

        with client.get(
                "<Add your API endpoint url here>", name=name, catch_response=True) as response:
            if response.status_code == 200:
                response.success()

                result = json.loads(response.content)
                # Success (T/F), response
                return True, result
            else:
                return False, None

    def add(self, client, userId, points, name="Add points"):
        endpoint = endpoints[self.region]['add']

        headers = {'Content-type': 'application/json'}
        body = json.dumps(
            {"userId": userId, "points": points})

        with client.post(url="<Add your API endpoint url here>", data=body, name=name,
                         headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()

                result = json.loads(response.content)
                return True, result
            else:
                return False, None

    def reduce(self, client, userId, points, name="Reduce points"):
        endpoint = endpoints[self.region]['reduce']

        headers = {'Content-type': 'application/json'}
        body = json.dumps(
            {"userId": userId, "points": points})

        with client.post(url="<Add your API endpoint url here>", data=body,
                         headers=headers, name=name, catch_response=True) as response:
            if response.status_code == 200:
                response.success()

                result = json.loads(response.content)
                return True, result
            else:
                return False, None

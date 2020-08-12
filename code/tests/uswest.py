import os
from datetime import datetime
import uuid
import json
import time

from locust import HttpUser, task, between, constant_pacing
from locust.contrib.fasthttp import FastHttpUser
from locust_plugins.csvreader import CSVReader

from common.helper import millis_interval
from common.api import Api
from common.logger import Logger

runId = os.environ.get("RUN_ID", uuid.uuid4())
filePath = os.environ.get("FILE_PATH", "logs/test")
logger = Logger(filePath, f"{runId}.csv")

data = CSVReader("data/users.csv")

region = "uswest"
api = Api(region)

class Read(HttpUser):

    # Please refer to https://docs.locust.io/en/stable/api.html#locust.wait_time.constant_pacing for docs
    wait_time = constant_pacing(0.01)

    def on_start(self):
        # Retrieve test data from csv
        user = next(data)
        self.userId = user[0]
        self.initPoints = user[1]
        self.pointsToAdd = user[2]

        success, balance, result = api.get(self.client, self.userId,
                                           name="Get initial user balance")
        self.currentBalance = balance

    @task(1)
    def get_balance(self):
        success, balance, result = api.get(
            self.client, self.userId)

        # Only log if the balance has changed
        if success and (self.currentBalance != balance):
            logger.logBalance(runId, 'GET', region, result)
            self.currentBalance = balance

    host = ""  # mandatory parameter, leave as blank

class Add(HttpUser):

    # Please refer to https://docs.locust.io/en/stable/api.html#locust.wait_time.constant_pacing for docs
    wait_time = constant_pacing(2)

    def on_start(self):
        # Retrieve test data from csv
        user = next(data)
        self.userId = user[0]
        self.initPoints = user[1]
        self.pointsToAdd = user[2]

    @task(1)
    def operations(self):
        success, result, requestKey = api.add(self.client, self.userId, self.pointsToAdd)
        if success:
            result['userId'] = self.userId
            result['pointsToAdd'] = self.pointsToAdd
            logger.logBalance(runId, 'ADD', region, result)

    host = ""  # mandatory parameter, leave as blank

class Reduce(HttpUser):

    # Please refer to https://docs.locust.io/en/stable/api.html#locust.wait_time.constant_pacing for docs
    wait_time = constant_pacing(6)

    def on_start(self):
        # Retrieve test data from csv
        user = next(data)
        self.userId = user[0]
        self.initPoints = user[1]
        self.pointsToReduce = user[2]

    @task(1)
    def operations(self):
        success, result, requestKey = api.reduce(self.client, self.userId, self.pointsToReduce)
        if success:
            result['userId'] = self.userId
            result['pointsToReduce'] = self.pointsToReduce
            logger.logBalance(runId, 'REDUCE', region, result)

    host = ""  # mandatory parameter, leave as blank



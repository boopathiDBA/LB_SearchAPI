import os
import requests

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities import parameters

tracer = Tracer()
metrics = Metrics()
logger = Logger(log_uncaught_exceptions=True)

OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST', 'https://search.stream.littlebirdie.dev/a_deals')
OPENSEARCH_INDEX = os.getenv('OPENSEARCH_INDEX', 'a_deals')

class Opensearch:
    # Class constructor (initializer method)
    def __init__(self, template, arguments):
        self.template = template
        self.arguments = arguments
        self.opensearch_host = OPENSEARCH_HOST
        self.opensearch_index = OPENSEARCH_INDEX

    # Class method
    def query(self):
        return f"OpenSearch host {self.opensearch_host} and OpenSearch Index {self.opensearch_index} using template {self.template} and arguments {self.arguments}."

@tracer.capture_method
def my_internal_func():

    try:
        response = requests.get(url=f'{OPENSEARCH_HOST}/{OPENSEARCH_INDEX}', headers = {"Accept": "application/json"}, timeout=5)
        logger.info(
            f"OpenSearch response: {response.content}"
            )
        return response.content
    except Exception as e:
        logger.error(
            f"Error: {e}"
            )
        return

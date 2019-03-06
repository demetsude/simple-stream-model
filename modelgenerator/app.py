'''
    This application is designed to simulate model generation.
    It periodically sends a randomly selected model from a set of
    models given in the challenge through a Kafka stream with the
    topic MODEL_TOPIC, which is specified in "docker-compose.yml".
    The frequency of sending a model is also specified with
    environment parameter MODEL_PER_SECOND in the same file.
'''

import os
import json
from time import sleep
from kafka import KafkaProducer
from random import randint

TOPIC = os.environ.get('MODEL_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
MODEL_PER_SECOND = float(os.environ.get('MODEL_PER_SECOND'))
SLEEP_TIME = 1 / MODEL_PER_SECOND

models = [{'model_weights': [8.46, 1.74, 6.08, 4.25, 1.92],
           'bias': 71.37},
          {'model_weights': [6.53, 5.46, 0.0, 9.95, 6.29],
           'bias': 43.3},
          {'model_weights': [3.2, 7.32, 1.46, 2.29, 4.26],
           'bias': 94.81},
          {'model_weights': [2.71, 0.82, 8.54, 0.21, 2.1],
           'bias': 66.25}]


if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    while True:
        model = models[randint(0, 100) % len(models)]
        producer.send(TOPIC, value=model)
        sleep(SLEEP_TIME)

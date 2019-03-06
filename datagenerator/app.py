'''
    This application is designed to simulate data generation.
    It periodically sends randomly generated data through a
    Kafka stream with the topic DATA_TOPIC, which is specified
    in "docker-compose.yml". The frequency of sending data is also
    specified with environment parameter DATA_PER_SECOND in the same file.
'''

import os
import json
from time import sleep
from kafka import KafkaProducer
from random import randint, uniform

TOPIC = os.environ.get('DATA_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
DATA_PER_SECOND = float(os.environ.get('DATA_PER_SECOND'))
SLEEP_TIME = 1 / DATA_PER_SECOND


def create_random_data():
    '''
        Creates random data
        Return:
            dict: {feature_vector: list, label: float}
    '''
    feature_vector = [round(uniform(-10, 10), 2) for i in range(0, 5)]
    data_record = {
        'feature_vector': feature_vector,
        'label': float(randint(0, 1))
    }
    return data_record


if __name__ == '__main__':
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    while True:
        data = create_random_data()
        producer.send(TOPIC, value=data)
        sleep(SLEEP_TIME)

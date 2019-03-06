import os
from predictor import Predictor

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
DATA_TOPIC = os.environ.get('DATA_TOPIC')
MODEL_TOPIC = os.environ.get('MODEL_TOPIC')
PREDICTION_TOPIC = os.environ.get('PREDICTION_TOPIC')
LOG_FILE = os.environ.get('LOG_FILE')

if __name__ == '__main__':

    pr = Predictor(KAFKA_BROKER_URL, DATA_TOPIC,
                   MODEL_TOPIC, PREDICTION_TOPIC,
                   LOG_FILE)
    pr.run()

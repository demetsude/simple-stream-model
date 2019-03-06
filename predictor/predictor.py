import json
import logging
from math import e
from kafka import KafkaConsumer, KafkaProducer


class Predictor:
    def __init__(self, kafka_broker, data_topic, model_topic,
                 prediction_topic, log_file):
        '''
            Class definition for the predictor
        '''
        # Configuration for Kafka
        self.kafka_broker = kafka_broker
        self.data_topic = data_topic
        self.model_topic = model_topic
        self.prediction_topic = prediction_topic
        self.topics = [self.model_topic, self.data_topic]

        self.consumer = KafkaConsumer(
            *self.topics,
            bootstrap_servers=self.kafka_broker,
            value_deserializer=lambda value: json.loads(value),)

        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_broker,
            value_serializer=lambda value: json.dumps(value).encode(),)

        # Configuration for Logging
        logging.basicConfig(
            filename=log_file,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        # Initialization of the model
        self.model = {'model_weights': [6.08, 7.78, 6.34, 8.05, 3.14],
                      'bias': 61.35}

        # Initialization of the packet count and the accuracy
        self.packet_count = 0
        self.correct_prediction = 0

    def predict(self, data):
        '''
            Issues predictions of the model on data and returns a prediction
            Input:
                dict: {feature_vector: list, label: float}
            Return:
                float, (0.0 or 1.0)
        '''
        data_features = data['feature_vector']
        model_weights = self.model['model_weights']
        dot_product = sum(i[0] * i[1] for i in
                          zip(data_features, model_weights))
        val = dot_product + self.model['bias']
        probability = 1.0 / (1.0 + e ** (-val))
        if probability > 0.5:
            return 1.0
        else:
            return 0.0

    def calculate_accuracy(self, label, prediction):
        '''
            Computes a running update of the accuracy
            Input:
                label: float, (0.0 or 1.0)
                prediction: float, (0.0 or 1.0)
            Return:
                dict: {packet_count: integer, accuracy: float}
        '''
        if (label == prediction):
            self.correct_prediction += 1
        accuracy = {"packet_count": self.packet_count,
                    "accuracy": float(self.correct_prediction) / self.packet_count}
        return accuracy

    def run(self):
        '''
           Listens the data and the model streams, and perform predictions.
           Logs the accuracy after every 10 predictions.
        '''
        for message in self.consumer:
            self.packet_count += 1
            if message.topic == self.data_topic:
                data = message.value
            elif message.topic == self.model_topic:
                self.model = message.value
            if self.packet_count > 0:
                prediction = self.predict(data)
                accuracy = self.calculate_accuracy(data['label'], prediction)
                if self.packet_count % 10 == 0:
                    logging.info(accuracy)
                    self.producer.send(self.prediction_topic, value=accuracy)

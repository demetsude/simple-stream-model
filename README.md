# Binary Classifier with Dynamic Models

A simple application to issue predictions of machine learning models on a stream of incoming data.

### Prerequisites
* [Docker](https://docs.docker.com/install/)

### System Design

* The whole system including a data generator, a model generator and the predictor application is designed within three different docker containers connected with Kafka streaming and configured in `docker-compose.yml`. 
	* `datagenerator` and `modelgenerator` work separately to send data and models to a stream with two different topics `DATA_TOPIC` and `MODEL_TOPIC`, respectively.

	* `predictor` reads the data and the models from these two topics through a Kafka stream. Whenever a new model is received, `predictor` updates its model and keep predicting with the new model without restarting. Additionally, the predictor computes a running update of the prediction accuracy and send it to the stream with a topic `PREDICTION_TOPIC`. It also logs the accuracy after every 10 predictions to `LOG_FILE`.

* Kafka broker and zookeper instances are also deployed as Docker containers configured in `docker-compose.kafka.yml`
* The project folder containing all components and configuration files is represented as

```
.
├── README.md
├── docker-compose.kafka.yml
├── docker-compose.yml
├── datagenerator 
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── modelgenerator
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── predictor
    ├── Dockerfile
    ├── app.py
    ├── predictor.py
    └── requirements.txt
```

### Running

* Starting Kafka cluster and the applications, run the following commands under the project folder:

	* Create Docker network: 
	`docker network create kafka-network`

	* Activate the Kafka cluster: 
	`docker-compose -f docker-compose.kafka.yml up -d`

	* Activate the applications:
	`docker-compose up`

	* To see the content of any stream, open another terminal and run the following command with changing `TOPIC_NAME`: 
	`docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic TOPIC_NAME --from-beginning`

		* `TOPIC_NAME` might be:
			* `queueing.model`
			* `queueing.data`
			* `streaming.prediction`

	* The accuracy log file is created in Docker container of `predictor` by default. To download the log file from the container to host:
		* List the `<containerID>` of the containers:
		`docker container ls`
		* Take the `<containerID>` of `predictor`.
		* Run the command by placing the `<containerID>`: 
    	`docker cp <containerID>:/usr/app/predictor.log  .`

* Stopping Kafka cluster and the applications:

	* To stop the applications:
	`docker-compose down`

	* To stop the Kafka cluster:
    `docker-compose -f docker-compose.kafka.yml stop`

### Notes

* For coding, PEP8 convention is followed.

# Welcome to FastAPI kafka stream processor

This application:
- consumes data on Kafka server
- source it to Delta Lake lakehouse for ML downstream tasks

## Run the app in local for event production/consumption

### Requirements
Python virtual environment can be setup as follows:

1. Install conda for Python virtual environment management
2. Install poetry for package management
3. Install just https://github.com/casey/just to use commands in the justfile.
4. run 
```
$ just install
```

### Run Kafka server
Run the Kafka server locally with
```
$ just kafka-server
```
from project root folder.

### add Kafka topics
```
$ just kafka-add-topics
```

### run the consumer app locally
```
$ just run-locally
```

### produce events in Kafka topics
For media radio events:
```
$ just kafka-produce-media-radio
```

For media tv events:
```
$ just kafka-produce-media-tv
```

For sales events:
```
$ just kafka-produce-sales
```

## Lakehouse

We will implement a medallion architecture.

### Bronze
Will receive consumed data from Kafka in raw event form.

### Silver
Will join consumed data from Kafka raw events in bronze stage to aggregate in silver stage.

### Gold
Will model data for feature store and ML downstream tasks.
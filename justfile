#!/usr/bin/env just --justfile
[private]
default:
  @just --list

# install the dependencies for the project
install:
	poetry install

# format code with black
format:
	poetry run black .

# test that the formatting is correct using black
format-test:
	poetry run black --check .

# run the tests
test:
	poetry run pytest -s tests/

# Run Kafka in a Docker container
kafka-server:
    docker run -p 2181:2181 -p 3030:3030 -p 8081-8083:8081-8083 \
       -p 9581-9585:9581-9585 -p 9092:9092 -e ADV_HOST=127.0.0.1 \
       lensesio/fast-data-dev:latest

# Add a new topic to Kafka
kafka-add-topics:
    kafka-topics --bootstrap-server localhost:9092 --create --topic media-radio-test --partitions 1

# Produce media channel radio test sample
kafka-produce-media-radio:
    jq -rc . tests/samples/media_channel_radio.json | kafka-console-producer --bootstrap-server localhost:9092 --topic media-radio-test

# Produce media channel tv test sample
kafka-produce-media-tv:
    jq -rc . tests/samples/media_channel_tv.json | kafka-console-producer --bootstrap-server localhost:9092 --topic media-tv-test

# Run the FastAPI app locally
run-locally:
	poetry run uvicorn app.main:app --port 8888 --reload

# Use the local installed binary to check consumer activity
kafka-consume-media-radio-test:
    kafka-console-consumer --bootstrap-server localhost:9092 --topic media-radio-test
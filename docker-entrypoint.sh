#!/bin/bash
set -ex

wait-for-it -t 40 ${IB_GATEWAY_HOST}:${IB_GATEWAY_PORT}
exec pipenv run python main.py

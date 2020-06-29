#!/bin/sh
mkdir -p .data/clickhouse-server
mkdir -p .data/grafana
mkdir -p .data/kafka
export UID=$(id -u)
export GID=$(id -g)
docker-compose -f docker-compose.yml up -d

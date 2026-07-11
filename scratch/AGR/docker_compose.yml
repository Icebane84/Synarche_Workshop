version: "3.9"

services:

  postgres:
    image: postgres:16

  clickhouse:
    image: clickhouse/clickhouse-server:latest

  nats:
    image: nats:latest
    command:
      - "-js"

  opa:
    image: openpolicyagent/opa

  prometheus:
    image: prom/prometheus

  grafana:
    image: grafana/grafana
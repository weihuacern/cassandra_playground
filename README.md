# Prometheus Playground

## Cassandra

```bash
pushd docker/
docker-compose -f ./compose.yml build cassandra
docker-compose -f ./compose.yml up -d cassandra
popd
```

## Metric Exporters
### Node Exporter
Monitor metrics for node. Service API on port 9100.

### Cadvisor
Monitor metrics for docker processes. Service API on port 9200.

```bash
pushd docker/
docker-compose -f ./exporter-compose.yml build node-exporter
docker-compose -f ./exporter-compose.yml build cadvisor
docker-compose -f ./exporter-compose.yml up -d node-exporter
docker-compose -f ./exporter-compose.yml up -d cadvisor
popd
```

## Prometheus and Grafana

```bash
pushd docker/
docker-compose -f ./compose.yml build prometheus
docker-compose -f ./compose.yml build grafana
docker-compose -f ./compose.yml up -d prometheus
docker-compose -f ./compose.yml up -d grafana
popd
```

[JMX Agent](https://www.robustperception.io/monitoring-cassandra-with-prometheus)

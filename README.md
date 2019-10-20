# Cassandra Playground

## Cassandra

```bash
pushd docker/
docker-compose -f ./compose.yml build cassandra
docker-compose -f ./compose.yml up -d cassandra
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

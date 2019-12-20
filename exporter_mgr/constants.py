from enum import Enum

class MetricExporterAction(Enum):
    CREATE = 1
    READ = 2
    UPDATE = 3
    DELETE = 4

CONTAINER_NAME_NODE_EXPORTER = "node-exporter"
CONTAINER_NAME_DOCKER_EXPORTER = "cadvisor"
IMAGE_NAME_NODE_EXPORTER = "prom/node-exporter"
IMAGE_NAME_DOCKER_EXPORTER = "google/cadvisor"
### Container name image name mapping
CONTAINER_NAME_IMAGE_NAME_MAP = {
    CONTAINER_NAME_NODE_EXPORTER: (IMAGE_NAME_NODE_EXPORTER, "v0.18.1"),
    CONTAINER_NAME_DOCKER_EXPORTER: (IMAGE_NAME_DOCKER_EXPORTER, "v0.33.0"),
}

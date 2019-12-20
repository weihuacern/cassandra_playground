from collections import deque

import fabric

from exporter_mgr.constants import (CONTAINER_NAME_NODE_EXPORTER, CONTAINER_NAME_DOCKER_EXPORTER,
                                    CONTAINER_NAME_IMAGE_NAME_MAP)
from exporter_mgr.logs import log_args

EXPORTER_HOME = "/opt/sys-monitor"
COMPOSE_FNAME = "exporter-compose.yml"

class MetricExporterManager():
    '''
    MetricExporterManager
    '''
    def __init__(self, cfg, src_dir):
        """
        Initialize the Metric Exporter Manager,
        with configuration
        source code dir
        """
        self.node_cfg_list = cfg.get('node_list')
        self.src_base_dir = f"{src_dir}"
        self.node_exec_plan = deque([
            CONTAINER_NAME_NODE_EXPORTER, # Node Exporter
            CONTAINER_NAME_DOCKER_EXPORTER, # Docker Exporter
        ])

    def create_exporters(self):
        """
        Create exporters on a list of nodes based on configuration
        """
        for node_cfg in self.node_cfg_list:
            self.create_node(node_cfg)

    def delete_exporters(self):
        """
        Delete exporters on a list of nodes based on configuration
        """
        for node_cfg in self.node_cfg_list:
            self.delete_node(node_cfg)

    @staticmethod
    def __connect_node(node_cfg):
        hostaddr = node_cfg.get("hostaddr")
        username = node_cfg.get("username")
        password = node_cfg.get("password")
        conn = fabric.Connection(hostaddr, port=22, user=username, connect_kwargs={'password': password})
        return conn

    def create_node(self, node_cfg):
        """
        Create exporters on one node
        provision -> bootup
        """
        with self.__connect_node(node_cfg) as conn:
            self._provision_node(conn, node_cfg)
            self._bootup_node(conn)

    def delete_node(self, node_cfg):
        """
        Delete exporters on one node
        shutdown -> unprovision
        """
        with self.__connect_node(node_cfg) as conn:
            self._shutdown_node(conn)
            self._unprovision_node(conn)

    def _provision_node(self, conn, node_cfg):
        """
        provision node to make sure it is ready for configure and boot up
        prepare installation dependencies
        """
        # NOTE, general prepare for a node
        conn.run(f"mkdir -p {EXPORTER_HOME}")
        # docker, docker-compose
        conn.run("docker --help")
        conn.run("docker-compose --help")

        hostaddr = node_cfg.get("hostaddr")
        username = node_cfg.get("username")
        password = node_cfg.get("password")

        conn.run(f"mkdir -p {EXPORTER_HOME}/docker")
        fpath = f"{self.src_base_dir}/docker/{COMPOSE_FNAME}"
        conn.local((f"sshpass -p \"{password}\" "
                    f"scp {fpath} {username}@{hostaddr}:{EXPORTER_HOME}/docker"))

    @staticmethod
    @log_args
    def __bootup_service(conn, compose_fname, container_name):
        conn.run(f"pushd {EXPORTER_HOME}/docker;\
            docker-compose -f ./{compose_fname} build --no-cache {container_name};\
            docker-compose -f ./{compose_fname} up -d {container_name};\
            popd;")

    def _bootup_node(self, conn):
        """
        Boot up exporters on one single node
        node exporter, docker exporter
        """
        compose_fname = COMPOSE_FNAME
        exec_plan = self.node_exec_plan.copy()
        while len(exec_plan) > 0:
            container_name = exec_plan.popleft()
            self.__bootup_service(conn, compose_fname, container_name)

    @staticmethod
    @log_args
    def __shutdown_service(conn, compose_fname, container_name):
        image_name, image_tag = CONTAINER_NAME_IMAGE_NAME_MAP.get(container_name)
        conn.run(f"pushd {EXPORTER_HOME}/docker;\
            docker-compose -f ./{compose_fname} stop {container_name};\
            docker-compose -f ./{compose_fname} rm -f {container_name};\
            docker rmi -f {image_name}:{image_tag};\
            popd;")

    def _shutdown_node(self, conn):
        """
        Shutdown exporters on one single node
        """
        compose_fname = COMPOSE_FNAME
        exec_plan = self.node_exec_plan.copy()
        while len(exec_plan) > 0:
            container_name = exec_plan.pop()
            self.__shutdown_service(conn, compose_fname, container_name)

    def _unprovision_node(self, conn):
        """
        Unprovision exporters for one single node
        """
        conn.run(f"rm -rf {EXPORTER_HOME}")

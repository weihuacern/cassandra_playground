import argparse
import json

from exporter_mgr.constants import MetricExporterAction
from exporter_mgr.logs import log_string
from exporter_mgr.metric_exporter_mgr import MetricExporterManager

def optparse():
    """
    Config input parameters for entrypoint
    """
    parser = argparse.ArgumentParser()
    action_string_list = [e.name for e in MetricExporterAction]
    parser.add_argument("-a", "--action", action="store",
                        help=f"Action taken for metric exporter: {action_string_list}")
    parser.add_argument("-c", "--cfgpath", action="store",
                        help="Absolute path of metric exporter configuration")
    parser.add_argument("-s", "--srcdir", action="store",
                        help="Absolute path of helios source code")
    return parser.parse_args()

def load_cfg_from_file(cfg_path):
    """
    Load compute cluster configuration from local file
    Input: cfg_path: configuration file path (json format for now)
    Output: cfg: configuration object (python dict for now)
    """
    with open(cfg_path) as cfg_file:
        cfg = json.load(cfg_file)
    return cfg

def entry():
    """
    Usage:
    1, To Create Metric Exporter with configuration:
    python3 target/exporter_mgr.pyz \
        -a CREATE \
        -c /root/prometheus_playground/exporter_mgr/sample_metric_exporter_cfg.json \
        -s /root/prometheus_playground

    2, To Delete Metric Exporter with configuration:
    python3 target/exporter_mgr.pyz \
        -a DELETE \
        -c /root/prometheus_playground/exporter_mgr/sample_metric_exporter_cfg.json \
        -s /root/prometheus_playground
    """
    options = optparse()
    action = options.action
    log_string(f"Action: {action}")
    if action in {MetricExporterAction.CREATE.name, MetricExporterAction.DELETE.name}:
        cfg = load_cfg_from_file(options.cfgpath)
        src_dir = options.srcdir
        log_string(f"Metric Exporter cfg: {cfg}")
        log_string(f"Source Code DIR: {src_dir}")
        me_mgr = MetricExporterManager(cfg, src_dir)
        if action == MetricExporterAction.CREATE.name:
            me_mgr.create_exporters()
        elif action == MetricExporterAction.DELETE.name:
            me_mgr.delete_exporters()
    else:
        log_string(f"Invalid action: {action}")

if __name__ == "__main__":
    entry()

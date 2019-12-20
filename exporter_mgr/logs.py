import inspect
import logging

LOG_DIR = "/var/log"
LOG_FNAME = "exporter-mgr.log"
logging.basicConfig(filename=f"{LOG_DIR}/{LOG_FNAME}", filemode='a', level=logging.INFO)

def log_args(func):
    """
    log_args: logging arguements before func get excuted
    """
    def wrapper(*args, **kwargs):
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str = ', '.join('{} = {!r}'.format(*item) for item in func_args.items())
        logging.info(f'{func.__module__}.{func.__qualname__} ( {func_args_str} )') # pylint: disable=logging-format-interpolation
        return func(*args, **kwargs)
    return wrapper

def log_string(string):
    logging.info(string)

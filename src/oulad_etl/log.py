import logging.config
import pathlib

import yaml


def setup_logging() -> None:
    cfg = pathlib.Path(__file__).parents[2] / "config/logging.yml"
    with cfg.open() as f:
        logging.config.dictConfig(yaml.safe_load(f))


setup_logging()
log = logging.getLogger("oulad")

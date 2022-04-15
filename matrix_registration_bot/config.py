import logging
import yaml
from os import environ


class Config(dict):
    """A class to manage the bot's configuration"""

    keys = ["BOT_SERVER", "BOT_USERNAME", "BOT_PASSWORD", "BOT_ACCESS_TOKEN",
            "API_BASE_URL", "API_TOKEN",
            "LOGGING_LEVEL"]

    def __init__(self, config_path=None):
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
        if config_path is not None:
            logging.info(f"Tying to load bot configuration from {config_path}")
            try:
                with open(config_path, 'r') as file:
                    self.extend_by_dict(yaml.safe_load(file))
            except FileNotFoundError:
                logging.error(f"Cold not find bot configuration at {config_path}")

        """
        This maps all self.keys (e.g. "LOGGING_LEVEL") that are in the environment to the corresponding config value
        e.g. self["logging"]["level"]. Does not support more than 2 level
        """
        for key in self.keys:
            scope, k = [x.lower() for x in key.split("_", maxsplit=1)]
            try:
                environ[key]
            except KeyError:
                logging.debug(f"{key} not set in environment")
                continue
            try:
                self[scope]
            except KeyError:
                self[scope] = {}
            self[scope][k] = environ[key]
            logging.debug(f"{key} set via environment")

        """Set the logging level according to config"""
        if self["logging"]['level'] in ["debug", "DEBUG"]:
            logging_level = logging.DEBUG
        elif self["logging"]['level'] in ["error", "ERROR"]:
            logging_level = logging.ERROR
        else:
            logging_level = logging.INFO
        logging.getLogger().setLevel(logging_level)

    def extend_by_dict(self, data):
        for key in data:
            self[key] = data[key]
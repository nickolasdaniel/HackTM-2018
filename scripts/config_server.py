import os
import sys
import json
import logging.config

from configparser import ConfigParser

logger = logging.getLogger(__name__+".config_server")
BASE_PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SERVER_CONFIG_FILE = os.path.join(BASE_PROJECT_FOLDER, "server_config.ini")
SERVER_LOGGER_FILE = os.path.join(BASE_PROJECT_FOLDER, "logging_server.json")

if os.path.exists(SERVER_LOGGER_FILE):
    with open(SERVER_LOGGER_FILE, "rt") as log_file:
        logging.config.dictConfig(json.load(log_file))
else:
    logging.basicConfig(level=logging.INFO)

if os.path.exists(SERVER_CONFIG_FILE):
    config_parser=ConfigParser()
    config_parser.read(SERVER_CONFIG_FILE)
else:
    logger.error("config file dosent exist")
    sys.exit(1)
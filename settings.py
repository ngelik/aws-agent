# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-

import argparse
import yaml
import pprint
from common import *


class Settings(object):
    def __init__(self, loggers):
        self.loggers = loggers
        self.settings = self._get_args()
        self.config = self.load_config()

    @timeit
    def _get_args(self):
        program = {'version': '1.0.0'}
        parser = argparse.ArgumentParser(description='%(prog)s, version - ' + program["version"],
                                         prog='AWS Agent', epilog="Good luck!")
        parser.add_argument("--file", '-f', type=str, required=True, dest='file',
                            help="File name with AWS Agent params", metavar='file_name')
        parser.add_argument('--post', '-p', action='store_true', required=False, dest='is_post',
                            help="Post data to Server")
        parser.add_argument('--debug', '-d', action='store_true', required=False, dest='is_debug',
                            help="Debug mode")

        return Mapping(**vars(parser.parse_args()))

    @timeit
    def load_config(self):
        self.loggers.root_logger.info("Trying to load file: %r", self.settings.file)

        with open(self.settings.file, 'rt') as f:
            config = yaml.safe_load(f.read())

        config_mapping = Mapping(**config)
        self.loggers.root_logger.info("Config file for AWS Agent has been loaded")
        # self.loggers.root_logger.debug(pprint.pprint(config))

        return config_mapping

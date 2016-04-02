# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-
from common import *


class info_host(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting Host checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("Host checker done!")

    @timeit
    def run(self):
        info = dict()
        info['agent'] = {}
        # info['agent']['ver'] = self.settings.config.r2agent_version
        info['agent']['ver'] = self.settings.version
        info['agent']['hb'] = int(time.time())
        return info


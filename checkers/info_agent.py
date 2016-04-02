# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-
from common import *
import platform
import commands


class info_agent(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting Agent checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("Agent checker done!")

    @timeit
    def run(self):
        info = dict()
        info['host'] = {}
        info['host']['name'] = platform.uname()[1]
        info['host']['distr'] = ", ".join(platform.linux_distribution())
        info['host']['kernel'] = platform.release()
        info['host']['openssl'] = commands.getstatusoutput('dpkg -l openssl | tail -1 | awk \'{print $3}\'')[1]
        return info

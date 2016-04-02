# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-
from common import *
import commands
import os


class info_mybatis(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting MyBatis checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("MyBatis checker done!")

    @timeit
    def run(self):
        info = dict()
        if os.path.exists(self.checker_settings["mybatis_path"]):
            os.environ["PATH"] += ":" + self.checker_settings["mybatis_path"]
            os.environ["JAVA_HOME"] = self.checker_settings["java_path"]
            my_batis = commands.getstatusoutput('migrate info | grep "^MyBatis Migrations [0-9].*" | cut -f 3 -d \ ')[1]
            info['mybatis'] = {'ver': my_batis}
        else:
            info['mybatis'] = {'ver': 'not installed'}
        return info

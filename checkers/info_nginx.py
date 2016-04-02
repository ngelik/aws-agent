# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-
from common import *
import commands


class info_nginx(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting Nginx checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("Nginx checker done!")

    @timeit
    def run(self):
        info = dict()
        # ps = commands.getstatusoutput('which nginx')
        # self.loggers.root_logger.info(ps)
        if process_exists("nginx"):
            i = commands.getstatusoutput('/usr/sbin/nginx -v')[1]
        else:
            self.loggers.root_logger.info("Nginx doesn't installed!")
            i = ""
        info['nginx'] = {'ver': i.replace("nginx version: nginx/", "").strip()}
        return info


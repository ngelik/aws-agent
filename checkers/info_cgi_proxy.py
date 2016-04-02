# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-
from common import *
import commands
import os


class info_cgi_proxy(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting CGI Proxy checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("Info CGI Proxy done!")

    @timeit
    def run(self):
        info = dict()
        path = self.checker_settings["cgiproxy_path"]
        if os.path.isfile(path):
            cgi_ver = commands.getstatusoutput('head -3 '+path+' | tail -1')[1]
        else:
            cgi_ver = ""
        info['cgiproxy'] = {'ver': cgi_ver.replace("#   CGIProxy ", "").strip()}
        return info


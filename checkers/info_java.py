# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-
from common import *
import commands
import os
import re


class info_java(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting Java checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("Java checker done!")

    @timeit
    def run(self):
        info = dict()
        path = self.checker_settings["tomcat_setenv_path"]
        java_version = commands.getstatusoutput(self.checker_settings["java_path"] +
                                                "/bin/java -version 2>&1 | awk -F '\"' '/version/ {print $2}'")[1]
        xmx = xms = ""
        if os.path.isfile(path):
            lines = list(open(path, 'r'))
            for i in range(0, len(lines)):
                l = lines[i].strip()
                if l[:1] != "#" and l.find("-Xms") > 0:
                    if xms == "":
                        xms = re.sub(" .*", "", re.sub(".*Xms", "", l))
                    if xmx == "":
                        xmx = re.sub(" .*", "", re.sub(".*Xmx", "" ,l))
        info['java'] = {'xms': xms, 'xmx': xmx, 'ver': java_version}
        return info

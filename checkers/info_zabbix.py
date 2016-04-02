# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-
from common import *
import commands


class info_zabbix(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting Zabbix checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("Zabbix checker done!")

    @timeit
    def run(self):
        info = dict()
        # ps = commands.getstatusoutput('which zabbix_agent')[1]
        if process_exists("zabbix_agentd"):
            zabbix_ver = commands.getstatusoutput('/usr/bin/zabbix_agent -V | head -1 | sed s/.*agent\ v// | sed s/\(.*//')[1]
            zabbix_count = commands.getstatusoutput('ps aux | grep [z]abbix_agentd | wc -l')[1]
        else:
            zabbix_ver = zabbix_count = "not installed"
        info['zabbix'] = {'ver': zabbix_ver.strip(), 'num': zabbix_count.strip()}
        return info

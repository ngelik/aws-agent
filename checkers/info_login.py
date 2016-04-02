# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-
from common import *
import subprocess
import datetime


class info_login(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting Login checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("Login checker done!")

    @timeit
    def run(self):
        info = dict()

        last_login_user = subprocess.Popen("last | grep -v 'reboot' | head -n1 | awk '{print $1}'",
                                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        last_login_date = subprocess.Popen("last | grep -v 'reboot' | head -n1 | cut -c 44-49",
                                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        last_login_date = datetime.datetime.strptime(
            str(datetime.date.today().year) + " " + last_login_date.strip(), "%Y %b %d")
        last_login_date = str(last_login_date.strftime(self.checker_settings["login_time_format"]))

        info['last_login'] = {'date': last_login_date, 'user': last_login_user.strip()}

        return info


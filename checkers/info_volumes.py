# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-

from common import *
import os
import re


class info_volumes(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting Volumes checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("Volumes checker done!")

    @timeit
    def _dl(self, d):
        if d[0:2] == "sd":
            r = d[2]
        elif d[0:2] == "xv":
            r = d[3]
        else:
            r = d
        return r

    @timeit
    def run(self):
        info = dict()
        v = {}
        d = os.popen ("find /dev -maxdepth 1 -type b -name 'md*' -or -name 'xvd*' -or -name 'sd*' | sed \"s/\\/dev\\///\"").readlines()
        for i in d:
            vol = i.strip()
            vv = self._dl(vol)
            v[vv] = {}
            mn = os.popen("df -h | grep ^/dev/" + vol).readlines()
            sw = os.popen("cat /proc/swaps | grep ^/dev/" + vol).readlines()
            if len(mn) > 0:
                f = re.split(r' +', mn[0])
                v[vv]['mpoint'] = f[5].strip()
                v[vv]['usage'] = f[4]
            elif len(sw) > 0:
                sws = sw[0].split('\t')
                v[vv]['mpoint'] = 'swap'
                v[vv]['usage'] = str(int(float(sws[2])/float(sws[1])*100))+"%"
        m = os.popen("cat /proc/mdstat | grep ^md").readlines()
        for i in m:
            s = i.split(" ")
            for j in range(4, len(s)):
                ss = s[j].split("[")
            v[self._dl(ss[0])]['mpoint'] = s[0]
            v[s[0]]['status'] = s[2]
            v[s[0]]['type'] = s[3]
        info['volumes'] = v

        return info


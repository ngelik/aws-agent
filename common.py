# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-

import time
import importlib
import logging
import logging.config
import zipfile
import os
import xml.etree.ElementTree as et
import psutil
import MySQLdb


class Loggers(object):
    def __init__(self, log_config):
        logging.config.fileConfig(log_config)
        self.root_logger = logging.getLogger()
        self.file_logger = logging.getLogger("file")
        self.console_logger = logging.getLogger("console")


class Mapping:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def timeit(method):
    def timed(*args, **kw):
        Loggers('./etc/logging.conf').root_logger.debug('Started - %r (%r, %r)', method.__name__, args, kw)
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        Loggers('./etc/logging.conf').root_logger.debug('Finished - %r (%r, %r) %2.4f sec' %
                                                  (method.__name__, args, kw, te-ts))
        return result
    return timed


@timeit
def str_to_class(module_name, class_name, *params):
    try:
        module_ = importlib.import_module(module_name)
        try:
            return getattr(module_, class_name)(*params)
        except AttributeError:
            print('Class does not exist')
            return None
    except ImportError:
        print('Module does not exist')
        return None


@timeit
def find_str_in_file(file, string):
    for line in file:
        if line.find(string) >= 0:
            return line


@timeit
def get_data_from_file_in_zip(zip_file, file_for_find):
    try:
        zf = zipfile.ZipFile(zip_file, 'r')
        for name in zf.namelist():
            if name.find(file_for_find) >= 0:
                return zf.read(name).split("\n")
    except Exception, e:
        print (e)


@timeit
def read_xml(file):
    if os.path.isfile(file):
        tree = et.parse(file)
        return tree.getroot()
    else:
        print "File %r doesn't exist!" % file


@timeit
def find_file_in_dir(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


@timeit
def process_exists(name):
    for p in psutil.process_iter():
        try:
            process = psutil.Process(p.pid)
            if process.name == name:
                return True
        except psutil.NoSuchProcess:
            pass
    return False


@timeit
def db_connect(host, user, passw, db, port):
    con = MySQLdb.connect(
        host=host,
        user=user,
        passwd=passw,
        db=db,
        port=port)

    if con.open:
        Loggers('./etc/logging.conf').root_logger.info(
            "Connected to MySQL database: %s@%s:%s/%s",
            user, host, port, db)

    return con
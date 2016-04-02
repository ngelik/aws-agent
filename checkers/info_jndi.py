# -*- coding: utf-8 -*-м# -*- coding: utf-8 -*-
from common import *


class info_jndi(object):
    def __init__(self, settings, checker_settings, loggers):
        self.settings = settings
        self.loggers = loggers
        self.checker_settings = checker_settings
        self.loggers.root_logger.info("Starting JNDI checker...")

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("JNDI checker done!")

    @timeit
    def run(self):
        info = dict()
        jndi_info = dict()

        for context_file in self.checker_settings["context_files"]:
            try:
                full_context_path = find_file_in_dir(context_file, self.checker_settings["context_find_path"])
                self.loggers.root_logger.info("Trying to get JNDI from file: %s, with full path: %s" % (context_file, full_context_path))
                if (full_context_path is not None) and os.path.isfile(full_context_path):
                    context_data = read_xml(full_context_path)
                    for child in context_data:
                        if child.tag == "Environment":
                            self.loggers.root_logger.debug("JNDI name: %r, value: %r" % (child.attrib['name'], child.attrib['value']))
                            jndi_info[child.attrib['name']] = child.attrib['value']
                            jndi_dict = dict()
                            jndi_dict["jndi"] = jndi_info
                            info.update(jndi_dict)
            except TypeError as e:
                self.loggers.root_logger.error("Error when get_jndi!")
                self.loggers.root_logger.error(type(e))
                self.loggers.root_logger.error(e.args)

        return info


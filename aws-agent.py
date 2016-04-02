from settings import *

import json
import pprint
import requests
import sys


class AWSAgent(object):
    @timeit
    def __init__(self):
        self.loggers = Loggers('./etc/logging.conf')
        self.loggers.root_logger.info("AWS Agent started!")
        self.loggers.root_logger.info('AWS gent params:\n %r', sys.argv)
        self.settings = Settings(self.loggers)
        self.settings.version = "1.0.0"

    def __enter__(self):
        return self

    @timeit
    def __exit__(self, type, value, traceback):
        self.loggers.root_logger.info("AWS Agent finished!")

    @timeit
    def r2post(self, method, agent_data):
        agent_data['user'] = self.settings.config.r2_user
        agent_data['pass'] = self.settings.config.r2_passw
        agent_data['id'] = requests.get(self.settings.config.meta_info_url).content
        data = json.dumps(agent_data)
        print requests.post(self.settings.config.r2_api_url + "/" +
                            method, data, headers=self.settings.config.r2_headers).content

    @timeit
    def run(self):
        agent_data = dict()
        for checker in self.settings.config.checkers:
            # agent_data.update(checkers.info_host(self.settings, checker, self.loggers).run())
            self.loggers.root_logger.info("Processing %r cheker...", checker["name"])
            info_checker_module = str_to_class(self.settings.config.r2_ckeckers_path + "." + checker["name"],
                                               checker["name"], self.settings, checker, self.loggers)
            with info_checker_module as info_checker_module:
                agent_data.update(getattr(info_checker_module, 'run')())

        if self.settings.settings.is_debug:
            print "debug:"
            pprint.pprint(agent_data)

        if self.settings.settings.is_post:
            self.r2post('agent-push', agent_data)


if __name__ == '__main__':
    with AWSAgent() as r2Agent:
        r2Agent.run()

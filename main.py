#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os

from pancakesbot.core import Core
from circuits import Manager, Worker

if __name__ == "__main__":
    debug = False

    config = {}
    if os.path.isfile('config.json'):
        with open('config.json') as config_file:
            config.update(json.load(config_file))

    # Set default log level to INFO and get some pretty formatting
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    manager = Manager()

    Worker(channel="pancakesbot").register(manager)
    Worker(channel="plugins").register(manager)

    Core(config).register(manager)

    if debug is True:
        from circuits import Debugger
        Debugger().register(manager)
    manager.run()

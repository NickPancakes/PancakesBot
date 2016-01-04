#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os

from pancakesbot.pancakesbot import PancakesBot

if __name__ == "__main__":
    debug = True

    config = {}
    if os.path.isfile('config.json'):
        with open('config.json') as config_file:
            config.update(json.load(config_file))

    bot = PancakesBot(**config)

    loglevel = logging.INFO
    if debug is True:
        from circuits import Debugger
        Debugger().register(bot)
        loglevel = logging.DEBUG

    logging.basicConfig(
        level=loglevel,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    bot.run()

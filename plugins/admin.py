#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from pancakesbot.baseplugin import BasePlugin


class AdminPlugin(BasePlugin):
    """The Admin Plugin has special commands only available to the user with the
    id set in self.admin_id. These revolve around plugin and user management
    """

    def init(self, bot, *args, **kwargs):
        super(AdminPlugin, self).init(bot, *args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.admin_id = 1

    def on_text(self, user, target, args):
        if (user[3] == self.admin_id) and (args.startswith('~')):
            args = args.split(' ')
            command = args[0][1:]
            args = args[1:]
            if command == "load":
                return self._load(user, target, args)
            elif command == "unload":
                return self._unload(user, target, args)
            elif command == "query":
                return self._query(user, target, args)
            elif command == "merge":
                return self._merge(user, target, args)
            elif command == "ids":
                return self._ids(user, target, args)

#####################
# Plugin Management #
#####################

    def _load(self, user, target, args):
        if not args:
            self.reply(user, target, "No plugins given.")
            return
        for plugin in args:
            try:
                self.bot.plugin_mngr.load(plugin)
                self.reply(user, target, "Plugin \"{}\" "
                                         "Successfully Loaded."
                                         .format(plugin))
            except Exception as e:
                self.reply(user, target, "Plugin \"{}\" "
                                         "Failed to Load - {}."
                                         .format(plugin, e))

    def _unload(self, user, target, args):
        if not args:
            self.reply(user, target, "No plugins given.")
            return
        for plugin in args:
            try:
                self.bot.plugin_mngr.unload(plugin)
                self.reply(user, target, "Plugin \"{}\" "
                                         "Successfully Unloaded."
                                         .format(plugin))
            except Exception as e:
                self.reply(user, target, "Plugin \"{}\" "
                                         "Failed to Unload - {}."
                                         .format(plugin, e))

    def _query(self, user, target, args):
        try:
            result = self.bot.plugin_mngr.query()
            loaded_plugins = []
            for plugin in result:
                plugin_name = plugin.split('.')[1]
                loaded_plugins.append(plugin_name)

            self.reply(user, target, "Loaded Plugins: {}"
                                     .format(', '.join(loaded_plugins)))
        except Exception as e:
            self.reply(user, target, "Unable to Query plugins. {}"
                                     .format(e))

#####################
# User Management #
#####################

    def _ids(self, user, target, args):
        ids = self.bot.user_mngr.get_ids()
        for user_id in ids:
            user_info = self.bot.user_mngr.user_from_id(user_id[0])
            self.reply(user, target, "{} : {}!{}@{}"
                                     .format(user_info[3],
                                             user_info[0],
                                             user_info[1],
                                             user_info[2]))

    def _merge(self, user, target, args):
        if len(args) != 2:
            self.reply(user, target, "Merging requires two nicknames.")
        elif args[0].isdigit() and args[1].isdigit():
            self.bot.user_mngr.merge_ids(int(args[0]), int(args[1]))
            self.reply(user, target, "Merging records of {} and {}."
                                     .format(args[0], args[1]))
        else:
            id0 = self.bot.user_mngr.id_from_nick(args[0])
            id1 = self.bot.user_mngr.id_from_nick(args[1])
            if id0 == id1:
                self.reply(user, target, "{} and {} are already merged."
                                         .format(args[0], args[1]))
            else:
                self.bot.user_mngr.merge_ids(id0, id1)
                self.reply(user, target, "Merging records of {} and {}."
                                         .format(args[0], args[1]))

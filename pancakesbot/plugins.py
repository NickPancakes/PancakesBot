#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from inspect import getmembers, isclass, getdoc
from importlib import import_module

from circuits import Component, handler
from circuits.tools import kill
from circuits.protocols.irc import PRIVMSG

from pancakesbot.baseplugin import BasePlugin


class PluginManager(Component):

    channel = "pancakesbot"

    def init(self, bot, command_prefix, plugin_prefix):
        self.logger = logging.getLogger(__name__)
        self.bot = bot
        self.command_prefix = command_prefix
        self.plugin_prefix = plugin_prefix
        self.loaded = {}
        self.commands = {}

    def reply(self, user, target, message):
        if target.startswith("#"):
            self.fire(PRIVMSG(target, message), "pancakesbot")
        else:
            self.fire(PRIVMSG(user, message), "pancakesbot")

    @handler("on_text", channel="plugins")
    def _on_text(self, user, target, message):
        nick_prefix = self.bot.nick + ": "
        if message.startswith(self.command_prefix):
            args = message[1:].split(' ')
        elif message.startswith(nick_prefix):
            prefix_len = len(nick_prefix)
            args = message[prefix_len:].split(' ')
        else:
            return
        command = args[0]
        if command == "help":
            self._print_help(user, target, args[1:])
        else:
            for plugin in self.commands:
                commands = self.commands[plugin]
                if command in commands:
                    func = commands[command]
                    self.logger.info("User {} ({}) "
                                     "Command \"{}\" "
                                     "Executing Plugin \"{}\""
                                     .format(user[0],
                                             user[3],
                                             command,
                                             plugin))
                    func(user, target, ' '.join(args[1:]))

    def _print_help(self, user, target, args):
        # general or command specific help
        if args:
            # Specific command
            for arg in args:
                if arg.startswith(self.command_prefix):
                    command = arg[1:]
                else:
                    command = arg
                for plugin in self.commands:
                    if command in self.commands[plugin]:
                        method = self.commands[plugin][command]
                        if hasattr(method, '__doc__'):
                            reply = "{}: {}".format(command, getdoc(method))
                        else:
                            reply = "No help text."
                        for line in reply.split('\n'):
                            self.reply(user, target, line)
        else:
            # List of commands
            for plugin in self.commands:
                commands_list = []
                plugin_name = plugin.split('.')[1]
                for command in self.commands[plugin]:
                    commands_list.append(self.command_prefix + str(command))
                self.reply(user,
                           target,
                           plugin_name + ': ' + ', '.join(commands_list))

    def load(self, plugin_name):
        try:
            fqplugin = "{0:s}.{1:s}".format(self.plugin_prefix, plugin_name)
            if fqplugin in sys.modules:
                self.logger.error("Plugin \"{}\": Unloading before reload."
                                  .format(plugin_name))
                self.unload(plugin_name)

            # Import plugin
            imported = import_module(fqplugin)
            self._load_members(fqplugin, imported)
        except Exception as e:
            self.logger.error("Plugin \"{}\": "
                              "Failed to Load: {} ".format(plugin_name,
                                                           e))
            raise

    def _load_members(self, fqplugin, imported):
        try:
            plugin_members = getmembers(imported, self._base_predicate)
            if not plugin_members:
                if fqplugin in sys.modules:
                    del sys.modules[fqplugin]
                raise TypeError("No members extended from BasePlugin")
            for name, PluginClass in plugin_members:
                instance = PluginClass(self.bot)
                if hasattr(instance, "register"):
                    instance.register(self)
                    self.logger.info("Plugin \"{}\": "
                                     "Registered \"{}\"."
                                     .format(fqplugin, instance))
                # Save loaded plugins
                if fqplugin not in self.loaded:
                    self.loaded[fqplugin] = set()
                self.loaded[fqplugin].add(instance)
                # Check for Commands
                for method_name in dir(instance):
                    method = getattr(instance, method_name)
                    if callable(method) and hasattr(method, 'commands'):
                        if fqplugin not in self.commands:
                            self.commands[fqplugin] = {}
                        for command in method.commands:
                            self.commands[fqplugin][command] = method
                            self.logger.info("Plugin \"{}\": "
                                             "Added Command \"{}\"."
                                             .format(fqplugin, command))
                self.logger.info("Plugin \"{}\": "
                                 "Loaded \"{}\"."
                                 .format(fqplugin, name))
            return True
        except Exception as e:
            self._clean_plugin(fqplugin, unload=True)
            self.logger.error("Plugin \"{}\": "
                              "Failed to members: {} ".format(fqplugin,
                                                              e))
            raise

    def _base_predicate(self, x):
        if isclass(x) and issubclass(x, BasePlugin):
            if x is not BasePlugin:
                return True
        return False

    def unload(self, plugin_name):
        try:
            fqplugin = "{0:s}.{1:s}".format(self.plugin_prefix, plugin_name)
            self._clean_plugin(fqplugin, True)
            self.logger.info("Plugin \"{}\": "
                             "Unload complete.".format(plugin_name))
            return True
        except Exception as e:
            self.logger.error("Plugin \"{}\": "
                              "Failed to Unload {}.".format(plugin_name, e))
            raise

    def _clean_plugin(self, fqplugin, unload=False):
        try:
            instances = self.loaded[fqplugin]
            for instance in instances:
                if hasattr(instance, "unregister"):
                    instance.unregister()
                kill(instance)
            del(instances)
            if fqplugin in self.commands:
                del self.commands[fqplugin]
            if fqplugin in self.loaded:
                del self.loaded[fqplugin]

            if unload is True:
                if fqplugin in sys.modules:
                    del sys.modules[fqplugin]
            self.logger.info("Plugin \"{}\": "
                             "Clean complete.".format(fqplugin))
        except Exception as e:
            self.logger.error("Plugin \"{}\": "
                              "Failed to clean {}.".format(fqplugin, e))
            raise

    def query(self):
        return self.loaded

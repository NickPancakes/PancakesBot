#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
from time import time
from signal import SIGINT, SIGTERM

from circuits import Component, handler, Timer, Event
from circuits.net.sockets import TCPClient, connect
from circuits.protocols.irc import (
    request, Message,
    IRC, NICK, USER, JOIN, QUIT,
    RPL_ENDOFMOTD, ERR_NICKNAMEINUSE, ERR_NOMOTD
)

import pancakesbot.events as events
from pancakesbot.users import UserManager
from pancakesbot.plugins import PluginManager


class PancakesBot(Component):

    channel = "pancakesbot"

    def init(self, **kwargs):
        # Default Settings
        prop_defaults = {
            'nick': "pancakesbot",
            'network': "irc.slashnet.org",
            'port': 6667,
            'channels': ["#bots"],
            'plugins': ['admin'],
            'plugins_path': 'plugins',
            'command_prefix': '~',
            'storage_path': 'storage'
        }
        self.__dict__.update(prop_defaults)
        # Overwrite defaults with kwargs
        if kwargs:
            self.__dict__.update(kwargs)

        self.terminate = False
        self.storage_path = os.path.abspath(self.storage_path)

        # Add a logger
        self.logger = logging.getLogger(__name__)

        # Add TCPClient and IRC to the system.
        TCPClient(channel=self.channel).register(self)
        IRC(channel=self.channel).register(self)

        # Creates an instance of UserManager
        self.logger.debug("Initializing user manager.")
        user_db_file = os.path.join(
            self.storage_path,
            'users-{}.db'.format(self.network)
        )
        self.user_mngr = UserManager(self, user_db_file)
        self.user_mngr.register(self)

        # Add plugins directory to path
        self.logger.debug("Initializing plugin manager.")
        self.plugins_path = os.path.abspath(self.plugins_path)
        sys.path.append(self.plugins_path)
        # Keeps track of plugins and commands
        self.plugin_mngr = PluginManager(self,
                                         self.command_prefix,
                                         os.path.basename(self.plugins_path)
                                         ).register(self)
        for plugin in self.plugins:
            self.plugin_mngr.load(plugin)

        # Send Keepalive PING every 5 minutes
        Timer(300.0, Event.create("keepalive"), persist=True).register(self)

    def keepalive(self):
        timestamp = int(time() * 1000)
        self.logger.debug("PING: {}".format(timestamp))
        self.fire(request(Message("PING", "LAG{0}".format(timestamp))))

    @handler("signal", channels="*")
    def signal(self, signo, stack):
        if signo in (SIGINT, SIGTERM):
            self.fire(QUIT("Received SIGTERM, terminating..."))
            self.fire(events.terminate())

    #######################################################
    # Event Handlers                                      #
    # These handle events and fire the pancakesbot events #
    #######################################################

    @handler("privmsg")
    def _on_text(self, user, target, message):
        user += (self.user_mngr.get_user_id(user), )
        if (message.startswith("\x01ACTION ")) and (message[-1] == '\x01'):
            message = message[7:]
            self.logger.debug("ACTION: {}({})@{}: {}".format(user[0],
                                                             user[3],
                                                             target,
                                                             message))
            self.fire(events.on_action(user, target, message), 'plugins')
        else:
            self.logger.debug("MSG: {}({})@{}: {}".format(user[0],
                                                          user[3],
                                                          target,
                                                          message))
            self.fire(events.on_text(user, target, message), 'plugins')

    @handler("ready")
    def _on_ready(self, component):
        self.logger.info("Ready. "
                         "Connecting to {0.network}:{0.port}"
                         .format(self))
        self.fire(connect(self.network, self.port))

    @handler("connected")
    def _on_connected(self, network, port):
        self.logger.info("Connected. Signing in as {0.nick}".format(self))
        self.fire(NICK(self.nick))
        self.fire(USER("pancakes", "pancakes", network, "robot"))
        self.fire(events.on_logon(network, port), 'plugins')

    @handler("disconnected")
    def _on_disconnected(self):
        self.logger.info("Disconnected.")
        self.fire(events.on_disconnect(), 'plugins')
        if self.terminate:
            raise SystemExit(0)
        else:
            self.logger.info("Reconnecting.")
            self.fire(events.on_reconnect(), 'plugins')
            self.fire(connect(self.network, self.port))

    @handler("terminate")
    def _on_terminate(self):
        self.terminate = True
        self.fire(events.on_exit(), 'plugins')
        self.logger.info("Terminating.")
        raise SystemExit(0)

    @handler("join")
    def _on_join(self, user, channel):
        user += (self.user_mngr.get_user_id(user), )
        self.fire(events.on_join(user, channel), 'plugins')
        self.logger.info("JOIN: {} ({}) to {}"
                         .format(user[0],
                                 user[3],
                                 channel))

    @handler("part")
    def _on_part(self, user, channel, *args):
        if args:
            message = args[0]
        else:
            message = ""
        user += (self.user_mngr.get_user_id(user), )
        self.fire(events.on_part(user, channel, message), 'plugins')
        self.logger.debug("PART: {} ({}) from {} ({})"
                          .format(user[0],
                                  user[3],
                                  channel,
                                  message))

    @handler("quit")
    def _on_quit(self, user, *args):
        if args:
            message = args[0]
        else:
            message = ""
        user += (self.user_mngr.get_user_id(user), )
        self.fire(events.on_quit(user, message), 'plugins')
        self.logger.debug("QUIT: {} ({})".format(user[0],
                                                 user[3],
                                                 message))

    @handler("notice")
    def _on_notice(self, user, target, message):
        user += (self.user_mngr.get_user_id(user), )
        self.fire(events.on_notice(user, target, message), 'plugins')
        self.logger.debug("NOTICE: {}@{}: {}"
                          .format(user[0],
                                  target,
                                  message))

    @handler("invite")
    def _on_invite(self, nickname, channel):
        user = self.user_mngr.get_full_user(nick=nickname)
        self.fire(events.on_invite(user, channel), 'plugins')
        self.logger.info("INVITE: {} ({}) invited us to {}."
                         .format(user[0],
                                 user[3],
                                 channel))

    @handler("kick")
    def _on_kick(self, user, channel, target, message):
        user += (self.user_mngr.get_user_id(user), )
        target = self.user_mngr.get_full_user(nick=target)
        self.fire(events.on_kick(user, target, channel, message), 'plugins')
        self.logger.debug("KICK: {} ({}) kicked {} ({}) from {} ({})"
                          .format(user[0],
                                  user[3],
                                  target[0],
                                  target[3],
                                  channel,
                                  message))

    @handler("mode")
    def _on_mode(self, user, target, mode, *args):
        if mode == "+b":
            user += (self.user_mngr.get_user_id(user), )
            self.fire(events.on_ban(user, args[0], target), 'plugins')
            self.logger.debug("BAN: {} banned {} from {}".format(user[0],
                                                                 args[0],
                                                                 target))
        elif mode == "-b":
            user += (self.user_mngr.get_user_id(user), )
            self.fire(events.on_unban(user, args[0], target), 'plugins')
            self.logger.debug("UNBAN: {} unbanned {} from {}".format(user[0],
                                                                     args[0],
                                                                     target))
        elif mode == "+v":
            user += (self.user_mngr.get_user_id(user), )
            t_user = self.user_mngr.get_full_user(nick=args[0])
            self.fire(events.on_voice(user, t_user, target), 'plugins')
            self.logger.debug("VOICE: {} gave voice "
                              "to {} in {}".format(user[0],
                                                   t_user[0],
                                                   target))
        elif mode == "-v":
            user += (self.user_mngr.get_user_id(user), )
            t_user = self.user_mngr.get_full_user(nick=args[0])
            self.fire(events.on_devoice(user, t_user, target), 'plugins')
            self.logger.debug("DEVOICE: {} removed voice "
                              "from {} in {}".format(user[0],
                                                     t_user[0],
                                                     target))
        elif mode == "+o":
            user += (self.user_mngr.get_user_id(user), )
            t_user = self.user_mngr.get_full_user(nick=args[0])
            self.fire(events.on_op(user, t_user, target), 'plugins')
            self.logger.debug("OP: {} gave operator "
                              "to {} in {}".format(user[0],
                                                   t_user[0],
                                                   target))
        elif mode == "-o":
            user += (self.user_mngr.get_user_id(user), )
            t_user = self.user_mngr.get_full_user(nick=args[0])
            self.fire(events.on_deop(user, t_user, target), 'plugins')
            self.logger.debug("DEOP: {} removed operator "
                              "from {} in {}".format(user[0],
                                                     t_user[0],
                                                     target))
        elif mode == "+q":
            user += (self.user_mngr.get_user_id(user), )
            t_user = self.user_mngr.get_full_user(nick=args[0])
            self.fire(events.on_owner(user, t_user, target), 'plugins')
            self.logger.debug("OWNER: {} gave owner "
                              "to {} in {}".format(user[0],
                                                   t_user[0],
                                                   target))
        elif mode == "-q":
            user += (self.user_mngr.get_user_id(user), )
            t_user = self.user_mngr.get_full_user(nick=args[0])
            self.fire(events.on_deowner(user, t_user, target), 'plugins')
            self.logger.debug("DEOWNER: {} removed owner "
                              "from {} in {}".format(user[0],
                                                     t_user[0],
                                                     target))
        elif target.startswith('#'):
            user += (self.user_mngr.get_user_id(user), )
            self.fire(events.on_mode(user, mode, target), 'plugins')
            self.logger.debug("MODE: {} set {} in {} ({})".format(user[0],
                                                                  mode,
                                                                  target,
                                                                  args))

    @handler("nick")
    def _on_nick(self, user, new_nick):
        self.user_mngr.changed_nick(user, new_nick)
        user += (self.user_mngr.get_user_id(user), )
        self.fire(events.on_nick(user, new_nick), 'plugins')
        self.logger.debug("NICK: {} ({}) changed nick to {}"
                          .format(user[0],
                                  user[3],
                                  new_nick))

    @handler("topic")
    def _on_topic(self, user, channel, topic):
        user += (self.user_mngr.get_user_id(user), )
        self.logger.debug("TOPIC: {} ({}) changed topic of {} to \"{}\""
                          .format(user[0],
                                  user[3],
                                  channel,
                                  topic))

    @handler("numeric")
    def _on_numeric(self, source, numeric, *args):
        self.logger.debug("NUMERIC: {} - {}".format(numeric, ', '.join(args)))

        if numeric == ERR_NICKNAMEINUSE:
            newnick = "{0:s}_".format(args[1])
            print(newnick)
            self.nick = newnick
            self.fire(NICK(newnick))
        elif numeric in (RPL_ENDOFMOTD, ERR_NOMOTD):
            self.fire(events.on_connect(self.network, self.port), 'plugins')
            for chan in self.channels:
                self.fire(JOIN(chan))

    # Used to test handlers to determine arguments
    @handler("test")
    def _gen_handler(self, *args, **kwargs):
        if args:
            for arg in args:
                self.logger.info("from args: {}".format(arg))
        if kwargs:
            for key, value in kwargs:
                self.logger.info("from kwargs: {} == {}".format(key, value))

# -*- coding: utf-8 -*-

from circuits import Component
from circuits.protocols.irc import (
    INVITE, JOIN, KICK, MODE, NICK,
    NOTICE, PART, PRIVMSG, TOPIC, QUIT
)


class BasePlugin(Component):

    channel = "plugins"

    def init(self, bot, *args, **kwargs):
        self.bot = bot
        self.bot_channel = self.bot.channel

    def ban(self, channel, user):
        if isinstance(user, tuple):
            self.mode(channel, '+b', "*!*@{}".format(user[2]))
        else:
            self.mode(channel, '+b', user)

    def deop(self, channel, user):
        if isinstance(user, tuple):
            self.mode(channel, '-o', user[0])
        else:
            self.mode(channel, '-o', user)

    def devoice(self, channel, user):
        if isinstance(user, tuple):
            self.mode(channel, '-v', user[0])
        else:
            self.mode(channel, '-v', user)

    def invite(self, nickname, channel):
        self.fire(INVITE(nickname, channel), self.bot_channel)

    def join(self, channels, keys=None):
        self.fire(JOIN(channels, keys), self.bot_channel)

    def kick(self, channel, user, comment=None):
        self.fire(KICK(channel, user, comment), self.bot_channel)

    def me(self, target, message):
        for line in message.split('\n'):
            line = "\x01ACTION {}\x01".format(line)
            self.msg(target, line)

    def mode(self, target, mode, *args):
        args = ' '.join(args)
        print(args)
        self.fire(MODE(target, mode, args), self.bot_channel)

    def msg(self, target, message):
        for line in message.split('\n'):
            if isinstance(target, tuple):
                self.fire(PRIVMSG(target[0], line), self.bot_channel)
            else:
                self.fire(PRIVMSG(target, line), self.bot_channel)

    def nick(self, nickname, hopcount=None):
        self.bot.nick = nickname
        self.fire(NICK(nickname, hopcount), self.bot_channel)

    def notice(self, receivers, message):
        for line in message.split('\n'):
            self.fire(NOTICE(receivers, line), self.bot_channel)

    def op(self, channel, user):
        if isinstance(user, tuple):
            self.mode(channel, '+o', user[0])
        else:
            self.mode(channel, '+o', user)

    def part(self, channels, message=None):
        print(message)
        if message is None:
            self.fire(PART(channels), self.bot_channel)
        else:
            self.fire(PART(channels, message), self.bot_channel)

    def reply(self, user, target, message):
        """Simplified msg that will respond to user or channel,
        whichever a message was sent from"""
        for line in message.split('\n'):
            if target.startswith("#"):
                self.msg(target, line)
            else:
                if isinstance(target, tuple):
                    self.msg(user[0], line)
                else:
                    self.msg(user, line)

    def topic(self, channel, topic=None):
        self.fire(TOPIC(channel, topic), self.bot_channel)

    def quit(self, message=None):
        self.fire(QUIT(message), self.bot_channel)
        raise SystemExit(0)

    def unban(self, channel, user):
        if isinstance(user, tuple):
            self.mode(channel, '-b', "*!*@{}".format(user[2]))
        else:
            self.mode(channel, '-b', user)

    def voice(self, channel, user):
        if isinstance(user, tuple):
            self.mode(channel, '+v', user[0])
        else:
            self.mode(channel, '+v', user)

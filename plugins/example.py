#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from circuits import handler

from pancakesbot.baseplugin import BasePlugin


class ExamplePlugin(BasePlugin):
    """Pancakesbot Plugin that utilizes all events and command functions.
    Serves as a testbed for everything that is set up in BasePlugin as well
    as a resource for anyone interested in writing a plugin."""

    def init(self, bot, *args, **kwargs):
        """Extends BasePlugin's init to create a logger."""
        super(ExamplePlugin, self).init(bot, *args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Example plugin loaded")

    def test_command(self, user, target, message):
        """Command used to test. Replies with user's ID.
        Usage: test"""
        self.reply(user, target, "Test Fired by {} (ID {})"
                                 .format(user[0], user[3]))
        self.logger.info("Test Fired by {} (ID {}) in {}: {}"
                         .format(user[0], user[3], target, message))
    test_command.commands = ['test', 't']

    #########################################################################
    # ----------------------------- Commands ------------------------------ #
    # The following use command syntax to use all of the functions built    #
    # into the BasePlugin class. Allows you to test each action and serves  #
    # as an example of how to create commands.                              #
    #########################################################################

    def ban_command(self, user, target, message):
        """Ban's the given nickname from the current channel.
        Usage: ban nickname"""
        # self.ban(channel, user):
        args = message.split(' ')
        if target.startswith('#'):
            if len(args) != 1:
                self.reply(user, target, "Invalid number of arguments")
            else:
                user_id = self.bot.user_mngr.id_from_nick(args[0])
                if user_id:
                    user = self.bot.user_mngr.user_from_id(user_id)
                    self.ban(target, user)
                else:
                    self.reply(user, target, "Nickname not of a known user.")
    ban_command.commands = ['ban']

    def deop_command(self, user, target, message):
        """Remove operator privileges from user in current channel.
        Usage: deop nickname"""
        # self.deop(channel, user):
        args = message.split(' ')
        if target.startswith('#'):
            self.deop(target, args[0])
    deop_command.commands = ['deop']

    def devoice_command(self, user, target, message):
        """Remove voice privileges from user in current channel.
        Usage: devoice nickname"""
        # self.devoice(channel, user):
        args = message.split(' ')
        if target.startswith('#'):
            self.devoice(target, args[0])
    devoice_command.commands = ['devoice']

    def invite_command(self, user, target, message):
        """Invites given nickname to given channel.
        Usage: invite nickname channel"""
        # self.invite(nickname, channel):
        args = message.split(' ')
        if len(args) != 2:
            self.reply(user, target, "Invalid number of arguments")
        else:
            self.invite(args[0], args[1])
    invite_command.commands = ['invite']

    def join_command(self, user, target, message):
        """Joins the given channel (with key if needed).
        Usage: join channel [key]"""
        # self.join(channels, keys=None)
        args = message.split(' ')
        if len(args) == 1:
            self.join(args[0])
        elif len(args) == 2:
            self.join(args[0], args[1])
        else:
            self.reply(user, target, "Invalid number of arguments")
    join_command.commands = ['join']

    def kick_command(self, user, target, message):
        """Kicks the given user from current channel with optional message.
        Usage: kick <nick> [message]"""
        # self.kick(channel, user, message)
        args = message.split(' ')
        if target.startswith('#'):
            if len(args) >= 2:
                self.kick(target, args[0], ' '.join(args[1:]))
            elif len(args) == 1:
                self.kick(target, args[0])
            else:
                self.reply(user, target, "Invalid number of arguments")
    kick_command.commands = ['kick']

    def me_command(self, user, target, message):
        """Says an ACTION in the current channel.
        Usage: me <message>"""
        # self.me(target, message)
        self.me(target, message)
    me_command.commands = ['me']

    def msg_command(self, user, target, message):
        """Messages the given target (channel or nick) with the given message.
        Usage: msg <target> <message>"""
        # self.msg(target, message):
        args = message.split(' ')
        if len(args) >= 2:
            self.me(args[0], ' '.join(args[1:]))
        else:
            self.reply(user, target, "Invalid number of arguments")
    msg_command.commands = ['msg']

    def nick_command(self, user, target, message):
        """Sets the nickname of the bot.
        Usage: nick <new_nicknname>"""
        # self.nick(nickname)
        args = message.split(' ')
        if len(args) == 1:
            self.nick(args[0])
        else:
            self.reply(user, target, "Invalid number of arguments")
    nick_command.commands = ['nick']

    def notice_command(self, user, target, message):
        """Notices the given target (channel or nick) with the given message.
        Usage: notice <target> <message>"""
        # self.notice(receivers, message)
        args = message.split(' ')
        if len(args) >= 2:
            self.notice(args[0], ' '.join(args[1:]))
        else:
            self.reply(user, target, "Invalid number of arguments")
        return
    notice_command.commands = ['notice']

    def op_command(self, user, target, message):
        """Give operator privileges from user in current channel.
        Usage: op nickname"""
        # self.op(channel, user):
        args = message.split(' ')
        if target.startswith('#'):
            self.op(target, args[0])
    op_command.commands = ['op']

    def part_command(self, user, target, message):
        """Parts the given channel (with message if given).
        Usage: part channel [message]"""
        # self.part(channels, message)
        args = message.split(' ')
        print(args)
        if len(args) == 1:
            self.part(args[0])
        elif len(args) >= 2:
            self.part(args[0], ' '.join(args[1:]))
        else:
            self.reply(user, target, "Invalid number of arguments")
    part_command.commands = ['part']

    def topic_command(self, user, target, message):
        """Sets the topic of current channel.
        Usage: topic <new_topic>"""
        # self.topic(channel, topic)
        if message:
            self.topic(target, message)
    topic_command.commands = ['topic']

    def quit_command(self, user, target, message):
        """Makes bot quit and exit with optional message.
        Usage: quit [message]"""
        # self.quit(user, target, args)
        if message:
            self.quit(message)
        else:
            self.quit()
    quit_command.commands = ['quit']

    def unban_command(self, user, target, message):
        """Unban's the given nickname from the current channel.
        Usage: unban nickname"""
        # self.unban(channel, user):
        args = message.split(' ')
        if target.startswith('#'):
            if len(args) != 1:
                self.reply(user, target, "Invalid number of arguments")
            else:
                user_id = self.bot.user_mngr.id_from_nick(args[0])
                if user_id:
                    user = self.bot.user_mngr.user_from_id(user_id)
                    self.unban(target, user)
                else:
                    self.reply(user, target, "Nickname not of a known user.")
    unban_command.commands = ['unban']

    def voice_command(self, user, target, message):
        """Give user voice privileges in current channel.
        Usage: voice nickname"""
        # self.voice(channel, user):
        args = message.split(' ')
        if target.startswith('#'):
            self.voice(target, args[0])
    voice_command.commands = ['voice']

    #########################################################################
    # ------------------------------ Events ------------------------------- #
    # These functions will trigger in response to events corresponding to   #
    # their name. Each event here will log when it has been triggered.      #
    # Custom function names can also be used with the circuits @handler     #
    # decorator. See the on_action event as an example of this.             #
    #########################################################################

    @handler("on_action")
    def custom_action(self, user, target, message):
        """on_action Event
        /me or /describe event received.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - string - Channel or User message was sent to.
            message - string - Full message received.
        """
        self.logger.info("ACTION: {}({})@{}: {}"
                         .format(user[0],
                                 user[3],
                                 target,
                                 message))

    def on_ban(self, user, channel, target):
        """on_ban Event
        User banned from a channel
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - string - Banned target.
            channel - string - Channel target is banned from.
        """
        self.logger.info("BAN: {} banned {} in {}".format(user[0],
                                                          target,
                                                          channel))

    def on_connect(self, network, port):
        """on_connect Event
        Successfully connected to IRC server and recieved it's MOTD.
        Args:
            network - string - IRC server address.
            port - int - Connection port of IRC server.
        """
        self.logger.info("Connect: {}:{}".format(network,
                                                 port))

    def on_deop(self, user, target, channel):
        """on_deop Event
        User has taken away operator privileges from target in channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel target is no longer operator of.
        """
        self.logger.info("DEOP: {} deopped {} in {}".format(user[0],
                                                            target[0],
                                                            channel))

    def on_deowner(self, user, target, channel):
        """on_deowner Event
        User has taken away owner privileges from target in channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel target is no longer owner of.
        """
        self.logger.info("DEOWNER: {} deownered {} in {}".format(user[0],
                                                                 target[0],
                                                                 channel))

    def on_devoice(self, user, target, channel):
        """on_devoice Event
        User has taken away voice privileges from target in channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel target is no longer voiced in.
        """
        self.logger.info("DEVOICE: {} devoiced {} in {}".format(user[0],
                                                                target[0],
                                                                channel))

    def on_disconnect(self):
        """on_disconnect Event
        Disconnected from IRC server.
        """
        self.logger.info("DISCONNECT")

    def on_exit(self):
        """on_exit Event
        Bot is exiting.
        """
        self.logger.info("EXIT")

    def on_invite(self, user, channel):
        """on_invite Event
        Received invite to join a channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel we've been invited to.
        """
        self.logger.info("INVITE: {} invited us to {}".format(user[0],
                                                              channel))

    def on_join(self, user, channel):
        """on_join Event
        User joined a channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel target was kicked from.
        """
        self.logger.info("JOIN: {} has joined {}".format(user[0],
                                                         channel))

    def on_kick(self, user, target, channel, message):
        """on_kick Event
        User kicked from a channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel target was kicked from.
            message - string - Kick message.
        """
        self.logger.info("KICK: {} kicked {} from {}: {}".format(user[0],
                                                                 target[0],
                                                                 channel,
                                                                 message))

    def on_logon(self, network, port):
        """on_logon Event
        PASS, NICK, and USER sent to server.
        Args:
            network - string - IRC server address.
            port - int - Connection port of IRC server.
        """
        self.logger.info("LOGON: {}:{}".format(network,
                                               port))

    def on_mode(self, user, mode, target,):
        """on_mode Event
        A channel mode has been changed.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            mode - string - Channel or user mode set.
            target - string - Chennel or Nickname affected.
        """
        self.logger.info("MODE: {} set mode {} on {}".format(user[0],
                                                             mode,
                                                             target))

    def on_nick(self, user, new_nick):
        """on_nick Event
        A user in a channel has changed their nick.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            new_nick - string - The new nickname.
        """
        self.logger.info("NICK: {} changed nick to {}".format(user[0],
                                                              new_nick))

    def on_notice(self, user, target, message):
        """on_notice Event
        Received a notice message.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - string - Channel or User that message was sent to.
            message - string - Full message received.
        """
        self.logger.info("NOTICE: {}@{}: {}".format(user[0],
                                                    target,
                                                    message))

    def on_op(self, user, target, channel):
        """on_op Event
        User has given target operator privileges in channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel target is operator of.
        """
        self.logger.info("OP: {} opped {} in {}".format(user[0],
                                                        target[0],
                                                        channel))

    def on_owner(self, user, target, channel):
        """on_owner Event
        User has given owner privileges from target in channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel target is owner of.
        """
        self.logger.info("OWNER: {} ownered {} in {}".format(user[0],
                                                             target[0],
                                                             channel))

    def on_part(self, user, channel, message):
        """on_part Event
        A user in a channel has parted the channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel that the user parted from.
            message - string - Part message.
        """
        self.logger.info("PART: {} parted from {}: {}".format(user[0],
                                                              channel,
                                                              message))

    def on_quit(self, user, message):
        """on_quit Event
        A user in a channel has quit IRC.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            message - string - Quit message.
        """
        self.logger.info("QUIT: {} has quit: {}".format(user[0],
                                                        message))

    def on_reconnect(self):
        """on_reconnect Event
        Disconnected and reconnected to an IRC server.
        """
        self.logger.info("RECONNECT")

    def on_text(self, user, target, message):
        """on_text Event
        Received private or channel message.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - string - Channel or User that message was sent to.
            message - string - Full message received.
        """
        self.logger.info("TEXT: {}@{}: {}".format(user[0],
                                                  target,
                                                  message))

    def on_topic(self, user, channel, topic):
        """on_topic Event
        A user has changed the topic of a channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel that the topic was changed.
            topic - string - The new topic.
        """
        self.logger.info("TOPIC: {} set topic of {} to {}".format(user[0],
                                                                  channel,
                                                                  topic))

    def on_unban(self, user, channel, target):
        """on_unban Event
        A user has been unbaned from a channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - string - Unbanned target.
            channel - string - Channel target is unbanned from.
        """
        self.logger.info("UNBAN: {} unbanned {} from {}".format(user[0],
                                                                target,
                                                                channel))

    def on_voice(self, user, target, channel):
        """on_voice Event
        User has given target voice privileges in channel.
        Args:
            user - tuple - (nickname, ident, hostname, user id)
            target - tuple - (nickname, ident, hostname, user id)
            channel - string - Channel target is voiced in.
        """
        self.logger.info("VOICE: {} voiced {} in {}".format(user[0],
                                                            target[0],
                                                            channel))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from circuits.core import Event


class terminate(Event):
    """terminate Event
    Disconnect, quit and close.
    """

#################
# Plugin Events #
#################


class on_action(Event):
    """on_action Event
    /me or /describe event received.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - string - Channel or User that is the target of the message.
        message - string - Full message received.
    """


class on_ban(Event):
    """on_ban Event
    User banned from a channel
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - string - Banned target.
        channel - string - Channel target is banned from.
    """


class on_connect(Event):
    """on_connect Event
    Successfully connected to IRC server and recieved it's MOTD.
    Args:
        network - string - IRC server address.
        port - int - Connection port of IRC server.
    """


class on_deop(Event):
    """on_deop Event
    User has taken away operator privileges from target in channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel target is no longer operator of.
    """


class on_deowner(Event):
    """on_deowner Event
    User has taken away owner privileges from target in channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel target is no longer owner of.
    """


class on_devoice(Event):
    """on_devoice Event
    User has taken away voice privileges from target in channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel target is no longer voiced in.
    """


class on_disconnect(Event):
    """on_disconnect Event
    Disconnected from IRC server.
    """


class on_error(Event):
    """on_error Event (incomplete)
    ERROR message from IRC server received.
    """


class on_exit(Event):
    """on_exit Event
    Bot is exiting.
    """


class on_invite(Event):
    """on_invite Event
    Received invite to join a channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel we've been invited to.
    """


class on_join(Event):
    """on_join Event
     User joined a channel.
     Args:
         user - tuple - (nickname, ident, hostname, user id)
         channel - string - Channel target was kicked from.
     """


class on_kick(Event):
    """on_kick Event
    User kicked from a channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel target was kicked from.
        message - string - Kick message.
    """


class on_logon(Event):
    """on_logon Event
    PASS, NICK, and USER sent to server.
    Args:
        network - string - IRC server address.
        port - int - Connection port of IRC server.
    """


class on_mode(Event):
    """on_mode Event
    A channel mode has been changed.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        mode - string - Channel or user mode set.
        target - string - Chennel or Nickname affected.
    """


class on_nick(Event):
    """on_nick Event
    A user in a channel has changed their nick.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        new_nick - string - The new nickname.
    """


class on_notice(Event):
    """on_notice Event
    Received a notice message.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - string - Channel or User that is the target of the message.
        message - string - Full message received.
    """


class on_op(Event):
    """on_op Event
    User has given target operator privileges in channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel target is operator of.
    """


class on_owner(Event):
    """on_owner Event
    User has given owner privileges from target in channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel target is owner of.
    """


class on_part(Event):
    """on_part Event
    A user in a channel has parted the channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel that the user parted from.
        message - string - Part message.
    """


class on_quit(Event):
    """on_quit Event
    A user in a channel has quit IRC.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        message - string - Quit message.
    """


class on_reconnect(Event):
    """on_reconnect Event (Incomplete)
    Disconnected and reconnected to an IRC server.
    """


class on_text(Event):
    """on_text Event
    Received private or channel message.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - string - Channel or User that is the target of the message.
        message - string - Full message received.
    """


class on_topic(Event):
    """on_topic Event
    A user has changed the topic of a channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel that the topic was changed.
        topic - string - The new topic.
    """


class on_unban(Event):
    """on_unban Event
    A user has been unbaned from a channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - string - Unbanned target.
        channel - string - Channel target is unbanned from.
    """


class on_voice(Event):
    """on_voice Event
    User has given target voice privileges in channel.
    Args:
        user - tuple - (nickname, ident, hostname, user id)
        target - tuple - (nickname, ident, hostname, user id)
        channel - string - Channel target is voiced in.
    """

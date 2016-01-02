#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import logging
from datetime import datetime

from circuits import Component


class UserManager(Component):

    channel = "bot"
    logger = None
    bot = None
    db_conn = None

    def init(self, bot, dbfile):
        """Initializes the logging and sets storage directory"""
        self.logger = logging.getLogger(__name__)
        self.bot = bot

        self.logger.info("Establishing Connection to User DB.")
        try:
            self.db_conn = sqlite3.connect(dbfile)
        except Exception:
            self.db_conn = None
            self.logger.exception("Unable to access local user database.")
            raise

        c = self.db_conn.cursor()
        # Primary Table
        c.execute("""
                  CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY NOT NULL,
                      last_nick TEXT COLLATE NOCASE,
                      last_ident TEXT COLLATE NOCASE,
                      last_vhost TEXT COLLATE NOCASE,
                      modified DATE,
                      created DATE
                  )
                  """)
        # nicks table
        c.execute("""
                  CREATE TABLE IF NOT EXISTS nicks (
                      id INTEGER PRIMARY KEY NOT NULL,
                      nick TEXT COLLATE NOCASE,
                      user_id INTEGER,
                      modified DATE,
                      created DATE,
                      FOREIGN KEY(user_id) REFERENCES users(id)
                  )
                  """)
        # vhosts table
        c.execute("""
                  CREATE TABLE IF NOT EXISTS vhosts (
                      id INTEGER PRIMARY KEY NOT NULL,
                      vhost TEXT COLLATE NOCASE,
                      user_id INTEGER,
                      modified DATE,
                      created DATE,
                      FOREIGN KEY(user_id) REFERENCES users(id)
                  )
                  """)
        self.db_conn.commit()

    def _update_nick(self, user_id, nick):
        c = self.db_conn.cursor()
        c.execute("""
                  UPDATE users SET
                      last_nick=?,
                      modified=?
                  WHERE id=?
                  """, (nick, datetime.utcnow(), user_id))
        c.execute("SELECT id FROM nicks WHERE nick=? AND user_id=?",
                  (nick, user_id))
        nick_exists = c.fetchone()
        if not nick_exists:
            c.execute("""
                      INSERT OR REPLACE INTO nicks (
                          nick,
                          user_id,
                          modified,
                          created
                      ) VALUES(?, ?, ?, ?)
                      """, (nick,
                            user_id,
                            datetime.utcnow(),
                            datetime.utcnow()))
        self.db_conn.commit()

    def _update_vhost(self, user_id, vhost):
        c = self.db_conn.cursor()
        c.execute("""
                  UPDATE users SET
                      last_vhost=?,
                      modified=?
                  WHERE id=?
                  """, (vhost, datetime.utcnow(), user_id))
        c.execute("SELECT id FROM vhosts WHERE vhost=? AND user_id=?",
                  (vhost, user_id))
        vhost_exists = c.fetchone()
        if not vhost_exists:
            c.execute("""
                      INSERT OR REPLACE INTO vhosts (
                          vhost,
                          user_id,
                          modified,
                          created
                      ) VALUES(?, ?, ?, ?)
                      """, (vhost,
                            user_id,
                            datetime.utcnow(),
                            datetime.utcnow()))
        self.db_conn.commit()

    def _new_user(self, user):
        # User DB
        c = self.db_conn.cursor()

        user_nick = user[0]
        user_host = user[1] + '@' + user[2]
        self.logger.info("NEW: Nick {}, Hostname {}"
                         .format(user_nick, user_host))
        # New User
        c.execute("""
                  INSERT OR REPLACE INTO users (
                      last_nick,
                      last_vhost,
                      modified,
                      created
                  ) VALUES(?, ?, ?, ?)
                  """, (user_nick,
                        user_host,
                        datetime.utcnow(),
                        datetime.utcnow()))
        user_id = c.lastrowid
        self.db_conn.commit()
        return user_id

    def changed_nick(self, user, nick):
        user_id = self.get_user_id(user)
        self._update_nick(user_id, nick)
        return user_id

    def get_full_user(self, nick=None, ident=None, hostname=None):
        user_id = self.get_user_id((nick, ident, hostname))
        return self.user_from_id(user_id)

    def get_user_id(self, user):
        if ((user[0] is not None) and
           (user[1] is not None) and
           (user[2] is not None)):
            # Full user
            return self.id_from_user(user)
        elif user[0] is not None:
            # Nick Only
            return self.id_from_nick(user[0])
        elif (user[1] is not None) and (user[2] is not None):
            # Vhost Only
            return self.id_from_vhost(user[1] + '@' + user[2])
        else:
            return None

    def id_from_user(self, user):
        # User DB
        c = self.db_conn.cursor()

        user_nick = user[0]
        user_host = user[1] + '@' + user[2]

        # Check what is and isn't already in the DB
        c.execute("SELECT user_id FROM vhosts WHERE vhost=?", (user_host,))
        id_vhost = c.fetchone()
        c.execute("SELECT user_id FROM nicks WHERE nick=?", (user_nick,))
        id_nick = c.fetchone()

        # If Nick and Vhost are both new, add a new user
        if id_vhost is None and id_nick is None:
            user_id = self._new_user(user)
        elif id_vhost is None:
            user_id = id_nick[0]
        elif id_nick is None:
            user_id = id_vhost[0]
        elif id_vhost == id_nick:
            user_id = id_vhost[0]
        else:
            # mismatched ids
            # TODO do something here?
            return None

        self._update_nick(user_id, user_nick)
        self._update_vhost(user_id, user_host)

        # all good, return ID
        return user_id

    def id_from_nick(self, nick):
        self.logger.debug("Getting user id for %s" % nick)
        c = self.db_conn.cursor()
        c.execute("SELECT user_id FROM nicks WHERE nick=?", (nick,))
        user_id = c.fetchone()
        if user_id:
            return user_id[0]
        else:
            return None

    def id_from_vhost(self, vhost):
        self.logger.debug("Getting user id for %s" % vhost)
        c = self.db_conn.cursor()
        c.execute("SELECT user_id FROM vhosts WHERE vhost=?", (vhost,))
        user_id = c.fetchone()
        if user_id:
            return user_id[0]
        else:
            return None

    def user_from_id(self, user_id):
        self.logger.debug("Recreating user from ID %s" % user_id)
        c = self.db_conn.cursor()
        c.execute('SELECT last_nick, last_vhost FROM users WHERE id=?',
                  (user_id,))
        user_data = c.fetchone()
        if user_data:
            split_vhost = user_data[1].split('@')
            user = (user_data[0], split_vhost[0], split_vhost[1], user_id)
            return user
        else:
            return None

    def merge_users(self, user1, user2):
        """Merges users, by full user or by nick"""
        if isinstance(user1, tuple):
            id1 = user1[3]
        else:
            id1 = self.id_from_nick(user1)

        if isinstance(user2, tuple):
            id2 = user2[3]
        else:
            id2 = self.id_from_nick(user2)

        return self.merge_ids(id1, id2)

    def merge_ids(self, id1, id2):
        if id1 > id2:
            user_from = self.user_from_id(id1)
            user_to = self.user_from_id(id2)
        elif id1 < id2:
            user_from = self.user_from_id(id2)
            user_to = self.user_from_id(id1)
        else:
            return False

        if (user_to is None) or (user_from is None):
            return False

        self.logger.debug("MERGE: from {}({}) to {}({})"
                          .format(user_from[0],
                                  user_from[3],
                                  user_to[0],
                                  user_to[3]))
        c = self.db_conn.cursor()
        c.execute("""
                  UPDATE nicks SET
                      user_id=?,
                      modified=?
                  WHERE user_id=?
                  """, (user_to[3], datetime.utcnow(), user_from[3]))
        c.execute("""
                  UPDATE vhosts SET
                      user_id=?,
                      modified=?
                  WHERE user_id=?
                  """, (user_to[3], datetime.utcnow(), user_from[3]))
        c.execute("DELETE FROM users WHERE id=?", (user_from[3],))
        self.db_conn.commit()
        return True

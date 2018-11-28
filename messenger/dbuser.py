import weakref

from messenger.user_status import UserStatus


class DBUserDict(dict):
    pass


class DBUser(object):
    def __init__(self, u_id, nickname):
        self._u_id = hash(nickname)
        self._nickname = nickname
        self._status = UserStatus.OFFLINE
        # set of DBUser (friends)
        self._fr_users = weakref.WeakSet()

    def add_user(self, user):
        if user not in self._fr_users:
            self._fr_users.add(user)
            user.add_user(self)

    def del_user(self, user):
        try:
            self._fr_users.remove(user)
        except KeyError:
            print "WARN: No such user for removing"

    def get_users(self):
        return self._fr_users

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, stat):
        self._status = stat

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, nick):
        self._nickname = nick

    def __hash__(self):
        return self._u_id
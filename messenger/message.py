from collections import defaultdict
from messenger.dbuser import DBUserDict
from messenger.utils import Enum


class MessageStatus(Enum):
    SENT = 1
    RECEIVED = 2


class MessageType(Enum):
    UNKNOWN_TYPE = 0
    INIT = 1
    STATUS = 2
    MESSAGE = 3
    ADD_FRIEND = 4
    DEL_FRIEND = 5


class MessageProcessor(object):
    def __init__(self):
        self._connected_users = DBUserDict()
        self._msg_queue = MessageQueue()

    def process_message(self, message):
        dbuser = self._connected_users.setdefault(nick, DBUser(None, nick))
        if msg_type == MessageType.STATUS:
            # statuses = connected_users.get_statuses()
            statuses = [{"nickname": friend.nickname, "status": friend.status}
                        for friend in dbuser.get_users()]
            resp = {"nickname": nick,
                    "friend": statuses}
            resp_json = json.dumps(resp)
            conn.send(resp_json)
        elif message.msg_type == MessageType.INIT:
            dbuser.status = parsed_data.get("status")
            conn_map[conn.fileno()] = dbuser
            print "{} connected status: {}".format(nick, UserStatus.to_string(dbuser.status))
        elif msg_type == MessageType.ADD_FRIEND:
            dbuser.status = parsed_data.get("status")
            print "{} connected status: {}".format(nick, UserStatus.to_string(dbuser.status))
        else:
            print "WARN: unknown message type"


class Message(object):
    def __init__(self, msg_type, sender, recipient, data):
        self._msg_type = msg_type
        self._recip = recipient
        self._data = data
        self._sender = sender

    @property
    def msg_type(self):
        return self._msg_type

    @msg_type.setter
    def msg_type(self, message_type):
        self._msg_type = message_type

    @property
    def recipient(self):
        return self._recip

    @recipient.setter
    def recipient(self, recip):
        self._recip = recip

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, obj_data):
        self._data = obj_data

    @property
    def sender(self):
        return self._data

    @sender.setter
    def sender(self, _sender):
        self._sender = _sender

    @classmethod
    def parse(cls, json_obj):
        msg_type = json_obj.get('type', MessageType.UNKNOWN_TYPE)
        try:
            recp = json_obj['recipient']
        except KeyError:
            recp = None
        if msg_type:
            return cls(msg_type, json_obj.get('nickname'), recp, json_obj)
        return None


class MessageQueue(object):
    def __init__(self):
        # {DBUser(): []}
        self._messages = defaultdict(set)

    def get_messages(self, user):
        return self._messages[user]

    def add_message(self, recipient, message):
        self._messages[recipient].add(message)

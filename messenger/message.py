import json
from collections import defaultdict
from messenger.dbuser import DBUserDict, DBUser
from messenger.user_status import UserStatus
from messenger.utils import Enum, JsonObject


class MessageStatus(Enum):
    SENT = 1
    RECEIVED = 2


class MessageType(Enum):
    UNKNOWN_TYPE = 0
    INIT = 1
    STATUS = 2
    MESSAGE = 3
    ADD_FRIEND = 4
    ADD_FRIEND_NOTIFY = 5
    ADD_FRIEND_ACCEPTED = 6
    ADD_FRIEND_DECLINED = 7
    DEL_FRIEND = 8


class MessageProcessor(object):
    def __init__(self):
        self._connected_users = DBUserDict()
        self._msg_queue = MessageQueue()

    def process_message(self, message, conn_sender):
        """
        Processing messages
        :param message: Message:
        :return:
        """
        nick = message.nickname
        msg_type = message.type
        dbuser, _ = self._connected_users.setdefault(nick,
                                                  (DBUser(None, nick), conn_sender))
        self._connected_users[nick] = (dbuser, conn_sender)
        if msg_type == MessageType.STATUS:
            # statuses = connected_users.get_statuses()
            statuses = [{"nickname": friend.nickname, "status": friend.status}
                        for friend in dbuser.get_users()]
            resp = {"nickname": nick,
                    "friend": statuses}
            resp_json = json.dumps(resp)
            conn_sender.send(resp_json)
        elif msg_type == MessageType.INIT:
            dbuser.status = message.status
            tx_message = Message()
            tx_message.type = MessageType.INIT
            tx_message.nickname = dbuser.nickname
            conn_sender.send(tx_message.to_json())
            print "{} connected status: {}".format(nick, UserStatus.to_string(dbuser.status))
        elif msg_type == MessageType.ADD_FRIEND:
            # {friend: nickname}
            # TODO Except case with non-existent DBUser
            recip = self._connected_users.get(message.recipient)
            if recip:
                user, conn_rec = recip
                assert user.nickname != nick
                tx_message = Message()
                tx_message.type = MessageType.ADD_FRIEND_NOTIFY
                tx_message.nickname = user.nickname
                tx_message.requester = nick
                conn_rec.send(tx_message.to_json())
        elif msg_type == MessageType.ADD_FRIEND_ACCEPTED:
            recip = self._connected_users.get(message.recipient)
            if recip:
                user, conn_rec = recip
                user.add_user(dbuser)
                tx_message = Message()
                tx_message.type = MessageType.ADD_FRIEND_ACCEPTED
                tx_message.nickname = user.nickname
                tx_message.requester = nick
                conn_rec.send(tx_message.to_json())
        else:
            print "WARN: unknown message type"


class Message(JsonObject):
    """
    Message of next struct
    {
        nickname: sender,
        recipient: rec_nickname [optional],
        type: message type,

        ===========
        some additional fields
        ===========
    }
    """
    def to_json(self):
        return json.dumps(self.__dict__)


class MessageQueue(object):
    def __init__(self):
        # {DBUser(): []}
        self._messages = defaultdict(set)

    def get_messages(self, user):
        return self._messages[user]

    def add_message(self, recipient, message):
        self._messages[recipient].add(message)

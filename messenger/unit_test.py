import unittest

from messenger.user_status import UserStatus
from messenger.dbuser import DBUser
from messenger.utils import JsonObject


class TestDBUser(unittest.TestCase):
    def test_db_user(self):
        u = DBUser(0, "nick1")
        u1 = DBUser(1, "nick2")
        u1.status = UserStatus.OFFLINE
        u.add_user(u1)
        for user in u.get_users():
            self.assertEqual(user.status, UserStatus.OFFLINE)

    def test_user_status(self):
        self.assertEqual(UserStatus.to_string(1),
                         "UserStatus.ONLINE")
        self.assertEqual(UserStatus.to_string(-1),
                         "UNKNOWN")


class TestJsonObj(unittest.TestCase):
    def test_json_obj(self):
        json_dict = {'field1': 1, 'field2': 2}
        self.assertEqual(JsonObject(json_dict).field1, 1)
        self.assertEqual(JsonObject(json_dict).field2, 2)
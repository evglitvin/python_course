import unittest

from messenger.main import UserStatus
from messenger.dbuser import DBUser


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
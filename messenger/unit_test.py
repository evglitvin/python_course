import unittest

from messenger.main import DBUser, UserStatus


class TestDBUser(unittest.TestCase):
    def test_db_user(self):
        u = DBUser(0)
        u1 = DBUser(1)
        u1.status = UserStatus.ONLINE
        u.add_user(u1)
        for user in u.get_users():
            self.assertTrue(user.status == UserStatus.OFFLINE,
                            "UserStatus not match")

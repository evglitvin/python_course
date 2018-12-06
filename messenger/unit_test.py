import os
import tempfile
import unittest
from contextlib import contextmanager
from io import IOBase

from messenger.user_status import UserStatus
from messenger.dbuser import DBUser
from messenger.utils import JsonObject, IndexedFile


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


class TestIndexedFile(unittest.TestCase):
    TEMP_DIR = tempfile.gettempdir()

    def _create_temp_indexed_file(self):
        _, name = tempfile.mkstemp(prefix='index')
        tmp_filename = os.path.join(self.TEMP_DIR, name + '.txt')
        ifile = IndexedFile(tmp_filename)
        ifile.writeline('hello')
        ifile.writeline('cruel world')
        ifile.writeline('mad world')
        ifile.writeline('the greatest world')

        ifile.close()
        return tmp_filename

    def test_creating_file(self):
        tmp_filename = self._create_temp_indexed_file()

        file_size = os.stat(tmp_filename).st_size
        ifile2 = IndexedFile(tmp_filename)
        idxs = sum(ifile2.read_indexes())
        ifile2.close()

        self.assertEqual(file_size, idxs)

    def test_reading_file(self):
        tmp_filename = self._create_temp_indexed_file()
        ifile = IndexedFile(tmp_filename)
        ifile.seek(0, 0)
        self.assertEqual(ifile.readline()[:-1], 'hello')
        self.assertEqual(ifile.readline()[:-1], 'cruel world')

        ifile.seek(0, 0)
        self.assertEqual(ifile.readline()[:-1], 'hello')

        ifile.seek(2, 1)
        self.assertEqual(ifile.readline()[:-1], 'the greatest world')

        ifile.seek(0, 0)
        ifile.seek(-1, 2)
        self.assertEqual(ifile.readline()[:-1], 'the greatest world')

        ifile.seek(0, 0)
        ifile.seek(-2, 2)
        self.assertEqual(ifile.readline()[:-1], 'mad world')

        ifile.close()

    def test_append_to_file(self):
        tmp_filename = self._create_temp_indexed_file()
        ifile = IndexedFile(tmp_filename)
        ifile.seek(0, 2)
        ifile.writeline('new line')

        ifile.close()

        ifile = IndexedFile(tmp_filename)
        ifile.seek(4, 0)
        self.assertEqual(ifile.readline()[:-1], 'new line')

        ifile.close()

    @contextmanager
    def test_context_file(self):
        tmp_filename = self._create_temp_indexed_file()
        with IndexedFile(tmp_filename) as ifile:
            ifile.readline()
            self.assertIsNotNone(ifile._file_obj)
        self.assertIsNone(ifile._file_obj)

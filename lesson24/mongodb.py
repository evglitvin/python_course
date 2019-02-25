from collections import deque
from multiprocessing.dummy import Pool

from pymongo import MongoClient


class Connection(object):
    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        db = self.connection['db1']
        self.tasks = db['table1']


class AsyncDB(object):
    def __init__(self, n=50):
        self.connections = deque([Connection()] * n)
        self.pool = Pool(n)

    def processing(self, func):
        conn = self.connections.popleft()
        ares = self.pool.apply_async(func, (conn,))
        return ares

    def return_connection(self, conn):
        self.connections.append(conn)


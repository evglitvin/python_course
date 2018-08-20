import hashlib
import os
from collections import defaultdict

import time


class Event(object):
    def __init__(self):
        self._type = None
        self._data = None

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    def set_type(self, _type):
        self._type = _type

    def set_data(self, data):
        self._data = data


class Observable(object):
    def __init__(self):
        self._objs = defaultdict(list)
        self.event = Event()

    def notifyall(self):
        for obj in self._objs[self.event.type]:
            obj.handle_event(self.event)

    def subscribe(self, event_type, observer):
        self._objs[event_type].append(observer)

    def unsubscribe(self, event_type, observer):
        pass


class Observer(object):
    def handle_event(self, event):
        raise NotImplementedError


class FileEventsType(object):
    FILE_CREATED = 1
    FILE_CHANGED = 2
    FILE_REMOVED = 3
    UNKNOWN_STATE = 0


class FileWatcher(Observable):
    def __init__(self):
        super(FileWatcher, self).__init__()
        self._path = {}

    def add_path(self, path):
        self._path[path] = (FileEventsType.UNKNOWN_STATE, 0)

    def _set_type_and_notify(self, file_path, file_state, _hash):
        self._path[file_path] = (file_state, _hash)
        self.event.set_type(file_state)
        self.event.set_data(file_path)
        self.notifyall()

    def run(self):
        while True:
            for file_path, (file_state, _hash) in self._path.iteritems():
                if not file_state:
                    if os.path.exists(file_path):
                        file_state = FileEventsType.FILE_CREATED
                        self._set_type_and_notify(file_path, file_state, _hash)
                else:
                    try:
                        with open(file_path) as fr:
                            hs = hashlib.md5(fr.read())

                            if _hash != hs.digest():
                                _hash = hs.digest()
                                file_state = FileEventsType.FILE_CHANGED
                                self._set_type_and_notify(file_path, file_state, _hash)
                    except IOError:
                        if file_state != FileEventsType.FILE_REMOVED:
                            file_state = FileEventsType.FILE_REMOVED
                            self._set_type_and_notify(file_path, file_state, _hash)
            time.sleep(5)


class FileChangedHandler(Observer):
    def handle_event(self, event):
        print self.__class__.__name__, event.type, event.data


class FileRemovedHandler(Observer):
    def handle_event(self, event):
        print self.__class__.__name__, event.type, event.data


if __name__ == "__main__":
    folder_path = '/home/lytvyn/courses/python_course/lesson7'
    f_watcher = FileWatcher()

    for file_path in os.listdir(folder_path):
        f_watcher.add_path(os.path.join(folder_path, file_path))

    f_watcher.subscribe(FileEventsType.FILE_CHANGED, FileChangedHandler())
    f_watcher.subscribe(FileEventsType.FILE_REMOVED, FileRemovedHandler())
    f_watcher.run()
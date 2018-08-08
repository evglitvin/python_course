# -*- coding: utf-8 -*-
import os


class UnknownID3TAG(Exception):
    pass


def get_int(data):
    val = 0
    shift = 0
    for b in data[::-1]:
        val = ord(b) << shift | val
        shift += 8
    return val


def read_id3(stream):
    data = stream.read(10)
    if len(data) == 10:
        id3 = data[0:3]
        version = data[3:5]
        flags = data[5]
        size = get_int(data[6:10])
        return id3, version, flags, size
    raise UnknownID3TAG


def decode(string_data, is_unicode, order=1):
    return string_data.decode('utf-16') if is_unicode else string_data


def read_tag(stream):
    data = stream.read(10)
    if len(data) == 10:
        tag_id = data[:4]
        if tag_id and get_int(tag_id) == 0:
            return (0,) * 3
        data_len = get_int(data[4:8])
        flags = get_int(data[8:10])
        return tag_id, data_len, flags


def read_str_tag(stream, data_len):
    """
    Returns decoded string
    :param stream: stream that should be read
    :param data_len: how many symbols should be read
    :return: decoded string
    """
    string_data = stream.read(data_len)
    if len(string_data) == data_len:
        is_unicode = ord(string_data[0])
        start_string = 1
        # according to spec here might be 3 letters of language wich ends with '00'
        if get_int(string_data[4:6]) == 0:
            start_string = 6
        return decode(string_data[start_string:], is_unicode)


class Mp3Info(object):
    def __init__(self, filepath):
        self._file = filepath
        self._title = None
        self._id3_version = None
        self._tags = {}

        self.read()

    def parse(self):
        pass

    def read(self):
        with open(self._file, 'rb') as stream:
            try:
                id3_info = read_id3(stream)
                self._id3_version = id3_info[0]
            except (UnknownID3TAG, OSError):
                return

            tag, size, flags = read_tag(stream)
            while tag:
                # ask for position in file
                pos = stream.tell()
                # trying to parse the string values
                self._tags[tag] = read_str_tag(stream, size)

                #set position to next tag
                stream.seek(pos + size, os.SEEK_SET)
                tag, size, flags = read_tag(stream)

    @property
    def album(self):
        return self._tags.get('TALB')

    @property
    def title(self):
        return self._tags.get('TIT2')

    @property
    def composer(self):
        return self._tags.get('TCON')


if __name__ == "__main__":
    # for dirpath, _, filenames in os.walk('/media/sf_Download1/'):
    filenames = u"""/media/sf_Download1/arash-feat.-mohombi-se-fue-radio-edit-(best-muzon.cc).mp3
    /media/sf_Download1/arilena-ara-nentori-bess-remix-(best-muzon.cc).mp3
    /media/sf_Download1/atb_all_i_need_is_you_feat_sean_ryan_(NaitiMP3.ru).mp3
    /media/sf_Download1/ATB – Desperate Religion (Integra Chill Mix).mp3
    /media/sf_Download1/estradarada-vite-nado-vyjjti-(best-muzon.cc).mp3
    /media/sf_Download1/Martin Merkel Feat. Malefiz - Voyager (Vocal Edit).mp3
    /media/sf_Download1/metallica_the_day_that_never_comes_(NaitiMP3.ru).mp3
    /media/sf_Download1/ofenbach-be-mine-(best-muzon.cc).mp3
    /media/sf_Download1/The xx - Intro (long version) by elkatheone (rappro.net).mp3
    /media/sf_Download1/vanotek-feat.-eneli-tell-me-who-deeperise-remix-(best-muzon.cc).mp3"""
    for f in filenames.encode('utf-8').split('\n'):
        # f_path = os.path.join(dirpath, f)
        # _, ext = os.path.splitext(f_path)
        # if ext == 'mp3':
        print f.strip()
        info = Mp3Info(f.strip())

        title = info.title
        album = info.album
        comp = info.composer
        print comp, album, title
    # s = '/media/sf_Download1/Martin Merkel Feat. Malefiz - Voyager (Vocal Edit).mp3'
    # print Mp3Info(s).title
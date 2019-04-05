from StringIO import StringIO
from cStringIO import StringIO as ctr
from zipfile import ZipFile

from lesson20.adv import get_bits_for_number, get_bits_count1

import struct
from socket import inet_aton

def playing_with_ip():
    ip = '123.45.46.245'

    # getting 4 bytes from ip address
    mbytes = [int(b) for b in ip.split('.')]
    ipaddr = 0
    for i, b in enumerate(mbytes):
        ipaddr = ipaddr | (b << ((len(mbytes) - i - 1) * 8))

    print bin(ipaddr)

    # forming mask
    0/24
    mask = ((1 << (32 - 24)) - 1) << 8
    print bin(mask)
    print bin(mask & ipaddr), mask & ipaddr


def diff_of_b_s_values():
    """
    Task from: https://telegra.ph/Anons-163-Pobitovaya-arifmetika---2-03-29
    """
    a = 786953

    print bin(a)
    print get_bits_for_number(a)
    print get_bits_count1(a)

    cb = get_bits_count1(a)
    minmask = ((1 << cb) - 1)
    mask = minmask << get_bits_for_number(a) - cb

    print mask, bin(mask)
    print minmask, bin(minmask)
    return mask - minmask


DASHED_STYLE = 0x1
DOTTED_STYLE = 0x2
SOLID_STYLE =  0x4

def line(point1, point2, style=0):
    if DASHED_STYLE & style:
        print "DASHED_STYLE"
    if DOTTED_STYLE & style:
        print "DOTTED_STYLE"
    if SOLID_STYLE & style:
        print "SOLID_STYLE"

line(0,0, DOTTED_STYLE | DASHED_STYLE)

f = StringIO()

zf = ZipFile(f, mode='w')
zf.write('__init__.py')
zf.close()

print f.getvalue()

# playing_with_ip()
from lesson20.adv import get_bits_for_number, get_bits_count1


def playing_with_ip():
    ip = '123.45.46.245'

    # getting 4 bytes from ip address
    mbytes = [int(b) for b in ip.split('.')]
    ipaddr = 0
    for i, b in enumerate(mbytes):
        ipaddr = ipaddr | (b << ((len(mbytes) - i - 1) * 8))

    print bin(ipaddr)

    # forming mask
    mask = (1 << (32 - 16)) - 1

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

diff_of_b_s_values()
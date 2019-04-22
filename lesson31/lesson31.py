

seq = "I am programmer"

# 775    FFFFFFFFFFFFFFFF
# 775    FFFFFFFF00FFFFFF
# 128    00FFFFFFFEFFFFFF
# 775    FFFFFFFF01FFFFFF

# print('{:X}'.format(int("FFF0 FFFF FEFF FFFF".replace(' ', ''), 16)))
(775, (1, 4))
(128, ())

def get_diff(iterable):
    res_dict = {}
    initials = {}
    for indata in iterable:
        in_data = indata.strip()
        if in_data:
            can_id, data = in_data.split()
            int_data = initials.get(can_id, int(data, 16))
            diff = res_dict.get(can_id, 0)
            res_dict[can_id] = diff | int_data ^ int(data, 16)
            initials[can_id] = int_data
    return res_dict

in_data = """
775    FFFFFFFFFFFFFFFF
775    FFFFFFFFAAFFFFFF
128    00FFFFFFFEFFFFFF
775    FFFFFFFFABFFFFF0
775    FFFFFFFFFFFFFFFF
128    01FFFFFFFEFFFFFF
"""
mask = 0xFF
diff_dict = get_diff(in_data.splitlines())
for k, v in diff_dict.items():
    list_items = list()
    for i in range(8):
        if mask & (v >> i * 8):
            list_items.append(i)

    diff_dict[k] = list_items

for k, v in diff_dict.items():
    print(k, v)
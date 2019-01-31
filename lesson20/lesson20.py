import sys
import time


def rotate_string(in_string):
    # Hello
    # elloH
    # lloHe
    while True:
        end_char = yield
        if end_char:
            yield in_string + end_char
        else:
            yield in_string
        in_string = in_string[1:] + in_string[0]


CH = '|\-/'

gen_rotate = rotate_string('Hello')
for idx, item in enumerate(gen_rotate):
    print gen_rotate.send('   ' + CH[idx % len(CH)])
    time.sleep(0.5)
    sys.stdout.write('\033[F')   # clears prev line . doesn't work in pycharm terminal

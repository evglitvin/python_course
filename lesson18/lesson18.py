import dis

a = 0
b = [0]


def func_add():
    global a, b
    a = a + 1
    b = []
    b.append('6')
    print b

func_add()
print b

print dis.dis(func_add)
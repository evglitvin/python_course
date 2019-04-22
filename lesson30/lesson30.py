import sys
print('Hello', file=sys.stderr )

# 2.x print >> sys.stderr, 'Hello'

print(5/2) # 2.0 5/2 == 2

d = {3: 6}

print(type(d.items())) # 2.0 list of all items

# raises TypeError
try:
    print(min([None, 3,6,2,7])) # 2.x returns none
except TypeError as e:
    print(e)

tup = (21,5,6,4)

a, *b, c = tup
print(b) # 2.0 SyntaxError: invalid syntax

class Meta(type):
    pass

class MyObject(metaclass=Meta):
    # 2.0 __metaclass__ = Meta
    pass

a = f"Jonny"
print(f'python {a[3]} new_style')

print(locals())

nonlocal f

class A(object):
    def __init__(self):
        print "init A"
        self.a = 0

    def handle(self):
        print "A"

class B(object):
    def __init__(self):
        print "init B"
        self.a = 1
    def handle(self):
        print "B"

#   X
#  / \
# A   B
#  \ /
#   C

class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        # super(A, self).__init__()


C().handle()


import sys
from cStringIO import StringIO

old_out = sys.__stdout__
my_out = StringIO()
sys.stdout = my_out

print "Hello world"
#  perform actions on stdout

sys.stdout = old_out

with open('traces.txt', 'w') as fw:
    fw.write(my_out.getvalue())
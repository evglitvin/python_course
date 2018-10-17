from pyparsing import *

test = """
Traceback (most recent call last):
    File "/home/lytvyn/python_course/lesson16/lesson16.py", line 8, in <module>
        a()
    File "/home/lytvyn/python_course/lesson16/lesson16.py", line 8, in a
"""

trace_string = """
Traceback (most recent call last):
  File "/home/lytvyn/python_course/lesson16/lesson16.py", line 8, in <module>
    print a()
  File "/home/lytvyn/python_course/lesson16/lesson16.py", line 7, in a
    5/0
ZeroDivisionError: integer division or modulo by zero
"""

def trace_parse(token):
    print token


trace = Keyword('Traceback')
empty_line = lineStart + SkipTo(lineEnd)
COLON = Literal(':').suppress()
COMMA = Literal(',').suppress()
start_trace = trace + SkipTo(COLON).suppress() + COLON
line = Keyword('line')
dig = Word(nums)
error = Word('.'+alphanums) + COLON

module = Word('.<>' + alphanums)
file_item = Keyword('File') + quotedString + COMMA + line + \
               dig + COMMA + Keyword('in') + module

bnf = (start_trace + OneOrMore(file_item) + error).setParseAction(trace_parse)
bnf.setDebug(True)
#
# for i in bnf.scanString(trace_string):
#     print i

for i in bnf.searchString(trace_string):
    print i


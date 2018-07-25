def get_simple_numpers(n):
    print "Start function"
    if n >= 2:
        yield 2
    print "before cycle"
    for number in xrange(3, n, 2):
        count = 0
        for divider in xrange(3, n/2, 2):
            if number % divider == 0:
                count += 1
                if count > 1:
                    break
        else:
            yield number
    print "after everything"

print sum(get_simple_numpers(20)) == 77


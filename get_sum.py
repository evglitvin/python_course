def get_sum(n):
    if n > 2:
        res_sum = 0
        for i in xrange(2, n + 1):
            for j in xrange(2, i):
                if i % j == 0:
                    break
            else:
                res_sum += i
        return res_sum
    else:
        print str(n) + 'Is no simple'


print get_sum(1000)

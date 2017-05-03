# Singled threaded 18.304428
# Multithreaded 7.442078

from __future__ import absolute_import, division, print_function

from builtins import range

import time
from multiprocessing import Pool

import numpy


def numpy_eval(value):
    
    for i in range(1000):
        value = numpy.tan(value)
        value = numpy.arctan(value)


    return value

a = [numpy.arange(10000) for _ in range(20)]


def test_singled_threaded():
    start = time.time()
    result = numpy_eval(a)
    end = time.time()
    print ('Singled threaded %f' % (end - start))


def test_multithreaded():
    pool = Pool(processes = 100)

    start = time.time()
    result = pool.map(numpy_eval, a)
    pool.close()
    pool.join()
    end = time.time()
    print ('Multithreaded %f' % (end - start))



if __name__ == '__main__':
    test_singled_threaded()
    test_multithreaded()

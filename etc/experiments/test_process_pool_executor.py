import concurrent.futures
import itertools
import os
import time

import numpy

SQUARE_LIST_SIZE = 20


def main():
    # Creates empty array.
    square_list = numpy.empty((SQUARE_LIST_SIZE, 2)) * 2

    # Creates a sequence (generator) of promises
    future_seq = make_future_seq(square_list)

    # Creates a sequence (generator) of computed square.
    square_seq = make_square_seq(future_seq)

    # Creates a sequence (generator) of computed square.
    square_list = list(square_seq)

    return square_list


def make_future_seq(squares):
    """
        Generates the sequence of empty a promises.
        Creates a new process only on `submit`.
    """

    with concurrent.futures.ProcessPoolExecutor(4) as executor:
        for i in range(SQUARE_LIST_SIZE):
            # Only makes a promise to do something.
            future = executor.submit(make_one_square, i, squares)
            print('future ', i, '= >', future)
            yield future


def make_square_seq(future_seq):
    """
        Generates the sequence of fulfilled a promises.
    """

    # Just to copy iterator
    for_show_1, for_show_2, future_seq = itertools.tee(future_seq, 3)

    # Let's check it, May be it withdrawn =)
    for i, future in enumerate(for_show_1):
        print('future ', i, 'done [1] =>', future.done())

    # Try to keep its promises
    for future in future_seq:
        yield future.result()

    # Let's check it one more time. It is faithful to!
    for i, future in enumerate(for_show_2):
        print('future ', i, 'done [2] =>', future.done())

    return future_seq


def make_one_square(i, squares):
    print('inside [1] = >', i, 'pid = ', os.getpid())
    squares[i, 0], squares[i, 1] = i, i ** 2

    time.sleep(1)  # Long and hard computation.

    print('inside [2]= >', i, 'pid = ', os.getpid())
    return squares


if __name__ == '__main__':
    main()



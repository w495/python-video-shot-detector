# -*- coding: utf8 -*-

import math
from itertools import izip

try:
    from scipy.stats.norm import logsf

except ImportError:
    def norm_cdf(z):
        """ Cumulative distribution for N(0, 1)
        :param z:
        """
        t = 1 / (1 + 0.2316419 * z)
        return (1 - 0.3989423 * math.exp(-z * z / 2) *
                ((((
                   1.330274429 * t - 1.821255978) * t + 1.781477937) * t - 0.356563782) * t + 0.319381530) * t)


    def logsf(z):
        """ Logarithm of the survival function for N(0, 1)
        :param z:
        :param z:
        """
        try:
            return math.log(1 - norm_cdf(z))
        except ValueError:
            return float('-inf')

norm_logsf = logsf

# Alignment costs: -100*log(p(x:y)/p(1:1))
bead_costs = {
    (1, 1): 0,
    (2, 1): 230,
    (1, 2): 230,
    (0, 1): 450,
    (1, 0): 450,
    (2, 2): 440
}

# Length cost parameters
mean_xy = 1
variance_xy = 6.8
LOG2 = math.log(2)


def length_cost(sx, sy):
    """ -100*log[p(|N(0, 1)|>delta)]
    :param sx:
    :param sy:
    :param sx:
    :param sy:
    """
    lx, ly = sum(sx), sum(sy)
    m = (lx + ly * mean_xy) / 2
    try:
        delta = (lx - ly * mean_xy) / math.sqrt(m * variance_xy)
    except ZeroDivisionError:
        return float('-inf')
    return -100 * (LOG2 + norm_logsf(abs(delta)))


def _align(x, y):
    m = {}
    for i in range(len(x) + 1):
        for j in range(len(y) + 1):
            if i == j == 0:
                m[0, 0] = (0, 0, 0)
            else:
                m[i, j] = min((m[i - di, j - dj][0] +
                               length_cost(x[i - di:i], y[j - dj:j]) +
                               bead_cost,
                               di, dj)
                              for (di, dj), bead_cost in
                              bead_costs.iteritems()
                              if i - di >= 0 and j - dj >= 0)

    i, j = len(x), len(y)
    while True:
        (c, di, dj) = m[i, j]
        if di == dj == 0:
            break
        yield (i - di, i), (j - dj, j)
        i -= di
        j -= dj


def char_length(sentence):
    """ Length of a sentence in characters
    :param sentence:
    :param sentence:
    """
    return sum(1 for c in sentence if c != ' ')


def align(sx, sy):
    """ Align two groups of sentences
    :param sx:
    :param sy:
    :param sx:
    :param sy:
    """
    cx = map(char_length, sx)
    cy = map(char_length, sy)
    for (i1, i2), (j1, j2) in reversed(list(_align(cx, cy))):
        yield ' '.join(sx[i1:i2]), ' '.join(sy[j1:j2])


def read_blocks(f):
    block = []
    for l in f:
        if not l.strip():
            yield block
            block = []
        else:
            block.append(l.strip())
    if block:
        yield block


def main(corpus_x, corpus_y):
    with open(corpus_x) as fx, open(corpus_y) as fy:
        for block_x, block_y in izip(read_blocks(fx), read_blocks(fy)):
            for (sentence_x, sentence_y) in align(block_x, block_y):
                print('%s ||| %s' % (sentence_x, sentence_y))


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        sys.stderr.write('Usage: %s corpus.x corpus.y\n' % sys.argv[0])
        sys.exit(1)
    main(*sys.argv[1:])

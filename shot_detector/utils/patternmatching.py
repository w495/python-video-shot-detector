from collections import defaultdict

class BadMatch(NameError):
    """Exception when your args don't match a pattern"""
    pass

class Any(object):
    """
    >>> 'wutup' == Any()
    True
    """
    def __eq__(mcs, _other):
        return True
Any = Any()

class OfType:
    """
    >>> 3 == OfType(int, str, bool)
    True
    >>> 'ok' == OfType(int)
    False
    """
    def __init__(self, *types):
        self.type = types
    def __eq__(self, other):
        return isinstance(other, self.type)

class Where:
    """
    >>> 'ok' == Where(str.isupper)
    False
    >>> [] == Where(len)
    False
    """
    def __init__(self, predicate):
        self.predicate = predicate

    def __eq__(self, other):
        try:
            return bool(self.predicate(other))
        except:
            return False

class WhereNot(Where):
    def __eq__(self, other):
        return not Where.__eq__(self, other)

class PatternMatcher(object):
    """
    Keeps a dict of lists where key is the function name
    and val is a list of functions with that name.

    Whenever it decorates a function, it adds that function
    to its dict of lists, then replace it with a new function
    that calls the right function in the list based on passed
    arguments.
    """

    def __init__(self):
        self.funcs = defaultdict(list)

    def find_match(self, name):
        """Return a function that knows how to call the right
        function based on the args passed in.
        """
        my_funcs = self.funcs[name]
        def wrapper(*args):
            # TODO: can we handle **kwargs??
            for function in my_funcs:
                if len(args) == len(function.__defaults__):
                    if all(passed == spec for (passed, spec) in zip(args, function.__defaults__)):
                        return function(*args)
            else:
                raise BadMatch("function `{0}` has no match for args ({1})".format(name, args))
        return wrapper

    def __call__(self, func):
        """Decorator: add to func to self.funcs"""
        keyword_args = func.__defaults__ or 0
        if func.__code__.co_argcount != len(keyword_args):
            raise SyntaxError("Every argument must have  default parameter for pattern matching")
        self.funcs[func.__code__.co_name].append(func)
        return self.find_match(func.__code__.co_name)

ifmatches = PatternMatcher()

if __name__ == "__main__":
    # pylint has NO IDEA what I'm doing here
    # it's all like 'OMGWTF?!'

    @ifmatches
    def my_func(test="hey"):
        print("this is my_func with test=hey")

    @ifmatches
    def my_func(test=2):
        print("this is my_func with test=2")

    @ifmatches
    def my_func(test=OfType(int)):
        print("this is my_func with int test!=2")

    @ifmatches
    def my_func(test=Any):
        print("this is my_func with a non-int")

    @ifmatches
    def psum(l=[]):
        return 0

    @ifmatches
    def psum(l=[Any]):
        return l[0]

    @ifmatches
    def psum(l=Where(lambda x: len(x) > 1)):
        head, tail = l[0], l[1:]
        return head + psum(tail)

    @ifmatches
    def count_letters(string=""):
        return 0
    @ifmatches
    def count_letters(string=OfType(str)):
        return count_letters(string[0], string[1:])
    @ifmatches
    def count_letters(x=Where(str.isalpha), xs=OfType(str)):
        return 1 + count_letters(xs)
    @ifmatches
    def count_letters(x=WhereNot(str.isalpha), xs=OfType(str)):
        return count_letters(xs)

    assert count_letters("ACD123") == 3
    assert count_letters("") == 0
    assert count_letters("123424") == 0
    try:
        count_letters(1)
        assert False
    except BadMatch:
        assert True

    import doctest
    doctest.testmod()

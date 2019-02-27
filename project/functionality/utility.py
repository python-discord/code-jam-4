import itertools


def pairwise(iterable):
    """
    Steps through an iterable while looking ahead
    one item every iteration.

    Example:
        for current, next in pairwise([1,2,3,4]):
            print(current, next)

        this would output:
        1 2
        2 3
        3 4
        4 None
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.zip_longest(a, b)
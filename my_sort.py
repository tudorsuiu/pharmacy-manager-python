def my_sort(iterable, *, key=lambda x: x, reverse=False):
    n = len(iterable)
    for i in range(n):
        for j in range(0, n - i - 1):
            if reverse:
                if key(iterable[j]) < key(iterable[j + 1]):
                    iterable[j], iterable[j + 1] = iterable[j + 1], iterable[j]
            else:
                if key(iterable[j]) > key(iterable[j + 1]):
                    iterable[j], iterable[j + 1] = iterable[j + 1], iterable[j]
    return iterable

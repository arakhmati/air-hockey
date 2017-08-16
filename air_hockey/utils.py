import collections

def flatten_list(x):
    if isinstance(x, collections.Iterable):
        return [a for i in x for a in flatten_list(i)]
    else:
        return [x]
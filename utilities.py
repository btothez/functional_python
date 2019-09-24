from functools import reduce, partial
from inspect import signature
from collections import OrderedDict, defaultdict
from config import Config
from pprint import pprint as pp


conf = Config()
INVALID_VALUES = conf.invalid_values


def curry(func):
    arity = lambda func: len(signature(func).parameters)
    def curried(*args):
        aty = arity(func)
        numargs = len(args)
        if aty <= numargs:
            return func(*tuple(args[0:aty]))
        return curry(partial(func, *tuple(args[0:aty])))
    return curried

def recursive_get(obj, lst):
    if len(lst) == 0:
        return obj
    if type(lst) != list:
        lst = [ lst ]
    return recursive_get(obj.get(lst[0], obj), lst[1:])



def list_pluck(key_list, lst):
    return map_list(
        lambda el: recursive_get(el, key_list),
        lst)

def tuple_map_list(func, lst):
    return map_list(
        lambda tup: func(tup[0], tup[1]),
        lst
    )


def add(x, y):
    return x + y

@curry
def filter_not_in(not_values, x):
    return x not in not_values

@curry
def filter_in(values, x):
    return x in values



def blackbird(reducer, mapper, init):
    return lambda lst: reduce(reducer, map(mapper, lst), init)

def normalizer(counter, keys):
    return blackbird(
        concat,
        lambda x: [float(counter[x]) / counter_sum(counter)],
        [])(keys)

def tuple_map_list(func, lst):
    return map_list(
        lambda tup: func(tup[0], tup[1]),
        lst
    )

def concat(lsta, lstb):
    return lsta + lstb

def implicit_conversion(s):
    if (s in INVALID_VALUES):
        return None
    elif type(s) in [int, float]:
        return s
    elif (str(s).isdigit()):
        return int(s)
    try:
        return float(s)
    except:
        return s

def counter_sum(cnt):
    return sum(cnt.values())

def set_list(lst):
    return list(set(lst))

def map_list(func, lst):
    return list(map(func, lst))

def filter_list(func, lst):
    return list(filter(func, lst))

def zip_list(lsts):
    return list(zip(*lsts))

def accumulator(acc, combo):
    acc[combo[0]].append(combo[1])
    return acc

def accumulate_dictionary(tuple_list):
    return reduce(
        accumulator,
        tuple_list,
        defaultdict(list))


def filter_map_list(filter_func, map_func, lst):
    return list(map(
        map_func, filter(filter_func, lst)
    ))

def filter_first(func, lst):
    return filter_list(func, lst)[0]

def first(lst):
    return lst[0]

@curry
def nth(n, lst):
    return lst[n]

def identity(x):
    return x

def compose2(f, g):
    return lambda x: f(g(x))

def compose(*functions):
    return reduce(
        lambda f, g: lambda x: compose2(f, g)(x),
        functions, identity)

def extendOD(ord_dict, lst):
    for el in zip(ord_dict, lst):
        ord_dict[el[0]].append(
            implicit_conversion(el[1])
        )
    return ord_dict


def extend(x, d):
    return OrderedDict(x, **d)



def float_conversion(s):
    try:
        return float(s)
    except:
        return s

char_clean = lambda c: str(c).replace('\xef\xbb\xbf', '')

def dict_map_tuple(key_func, val_func):
    tuple_it = lambda x: (key_func(x), val_func(x))
    return lambda lst: dict(map(tuple_it, lst))

def dict_map(func, gen):
    return dict(map(func, gen))

def dict_zip(lsta, lstb):
    return dict(zip(lsta, lstb))

def dict_list(itms):
    return dict(lst(lsta, lstb))


def split_double_underscore(x):
    return x.split('__')[1] if '__' in x else x

def dict_map_list(func, lst):
    return dict(map_list(func, lst))

@curry
def dict_map_items(key_func, val_func):
    process_tuple = lambda k, v: (key_func(k), val_func(v))
    return lambda d: dict(
        map_list(
            lambda item: process_tuple(*item),
            d.items()
        )
    )

def dict_map_identity(val_func):
    return dict_map_items(identity, val_func)

def dict_map_dict(val_func, dct):
    items = dct.items()
    return dict_map(
        lambda item: (item[0], val_func(item[0], item[1])),
        items)

def each_with_all_others(lst, excludes):
    all_others = lambda x: filter_list(lambda q: q != x, lst)
    excludeit = lambda lst: filter_list(filter_not_in(excludes), lst)
    support_drivers = map_list(
        compose(excludeit, all_others),
        lst
    )
    return zip_list([lst, support_drivers])

def zip_with_index(lst):
    return zip_list([range(len(lst)), lst])

def pp(obj):
    return pp(obj)

@curry
def get(attr, obj):
    return obj.get(attr)

@curry
def get_value(dictionary, key):
    return dictionary[key]


def flatfilter(lst_of_lsts):
    return [element for lst in lst_of_lsts for element in lst]

def flat_map_list(func, lst):
    return [n for el in map_list(func, lst) for n in el]

@curry
def get_list_of_vals_from_dict(lst, dct):
    return map_list(
        get_value(dct),
        lst
    )

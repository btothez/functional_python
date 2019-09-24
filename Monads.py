from functools import *

idn = lambda x: x
def compose(f, g):
    return lambda x: f(g(x))

def compose_list(lst):
    return reduce(lambda f,g: compose(f, g), lst)

class ContMonad:
    def __init__(self, cont=lambda a: a):
        self.func = cont

    def unit(self, val):
        return ContMonad(lambda cont: cont(val))

    def bind(self, bindee):
        def new_mon_function(cont):
            return self.func(lambda x: bindee(x)(cont))
        return ContMonad(lambda cont: new_mon_function(cont))

    def bind_list(self, bindee_list):
        return reduce(lambda cont_mon, bindee: cont_mon.bind(bindee), bindee_list, self)


"""
bindee1 = lambda x: lambda cont: cont(x + 15)
bindee2 = lambda x: lambda cont: cont(x * 15)
bindee_middle = 
cm = ContMonad()
cm.unit(10).bind(bindee1).bind(bindee2).func(print)

or:

def bind_middle(x):
    return lambda cont: cont(x) if x <=500 else "STOP, TOO BIG"
bindee3 = lambda x: lambda cont: cont(x/3.14)
bindee2 = lambda x: lambda cont: cont(x + 2)
bindee1 = lambda x: lambda cont: cont(x * 10)

cm.unit(50).bind_list([bindee1, bind_middle, bindee2, bindee3]).func(print)
    159.87261146496814

cm.unit(51).bind_list([bindee1, bind_middle, bindee2, bindee3]).func(print)
    Out[34]: 'STOP, TOO BIG'
"""



class StateMonad:
    def __init__(self, func=lambda state: (idn, state)):
        self.func = func 

    def unit(self, func):
        return StateMonad(func)

    def bind(self, bindee):

        def inner(state):
            tmp_func, tmp_state = self.func(state)
            fin_func, fin_state = bindee(tmp_state)
            return(compose(fin_func, tmp_func), fin_state)


        return StateMonad(inner)

"""

def func1(st):
    x = 'did this'
    st['out'] += x
    st['cnt'] += 1
    return (lambda x: '(' + x + ')', st)

def func2(st):
    x = 'another thing'
    st['out'] += x
    st['cnt'] += 1
    return (lambda x: ')' + x + '(', st)


initial_state = {
'out': '',
'cnt': 0}
st = StateMonad()
outfunc, outstate = st.bind(func1).bind(func2).func(initial_state)
"""


# First I need a way to do a continuation monad where the monadic value
# Stores a pipeline function
# Make State into a genuine algebraic datatype

"""
Combination Monad, 
takes a function like thi:
def bindee(state):
    def pipeline(dataframe):
        if state.add_column:
            dataframe.x = dataframe.old_column + 1
            state.new_columns.append('x')
        else:
            state.comments.append('There was no flag to add column')
        return dataframe

    def take_continuation(continuation):
        if len(state.comments) == 0:
            return continuation(pipeline)
        else:
            return pipeline

    return (take_continuation, state)
"""
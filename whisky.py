from __future__ import print_function
import time

try:
    import builtins
except ImportError:
    import __builtin__ as builtins


def drunk_import(name, *args, **kwargs):
    '''Like __import__(), but drinks every time this module is imported.'''
    if name == __name__:
        drink()
    return original_import(name, *args, **kwargs)

def drink(state={'count':0,'start':time.time()}):
    '''Drink responsibly.
    
       Python's default arguments are initialized only once, so it can be
       used like a static variable in C. This is used to preserve state
       across calls to the function to count the number of drinks and the
       time since drinking began.
    '''
    state['count'] += 1
    count = state['count']
    dt = time.time() - state['start']
    bac = ebac(state['count'], dt)
    print('woohoo', state['count'], bac)
    if 0.129 < bac < 0.138:
        print('bullseye')

def ebac(drinks, dt=0, weight=80, metabolism=0.017, water_ratio=0.58):
    '''Estimate BAC using Widmark's formula.'''
    return (0.806 * drinks * 1.2) /  (weight * water_ratio) - metabolism * dt


# I spent a while last night trying to get this to work using import hooks,
# but all of the hooks after modules are looked up in sys.modules. I tried
# to replace sys.modules with a "WhiskyDict" object that deleted the cache
# entry for this module after being accessed, which was breaking something
# deep inside the import mechanism. This is a lot simpler, to say the least.
original_import = __import__
builtins.__import__ = drunk_import
drink()

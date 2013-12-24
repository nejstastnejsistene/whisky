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
    bac = ebac(count, dt)
    # Can't have negative bac, restart the timer and recalculate.
    if bac <= 0:
        state['count'] = 0
        state['start'] = time.time()
        return drink()

    print('woohoo', count, bac)
    if 0.129 < bac < 0.138:
        print('bullseye')
    elif bac > 0.138:
        # So the tshirt script works.
        import os, sys
        sys.stdout = lambda x: sys.__stdout__.write(os.urandom(20) + '\n')

def ebac(drinks, dt=0, weight=80, metabolism=0.017, water_ratio=0.58):
    '''Estimate BAC using Widmark's formula.'''
    bac = (0.806 * drinks * 1.2) /  (weight * water_ratio) - metabolism * dt
    return max(bac, 0)


# I spent a while last night trying to get this to work using import hooks,
# but all of the hooks after modules are looked up in sys.modules. I tried
# to replace sys.modules with a "WhiskyDict" object that deleted the cache
# entry for this module after being accessed, which was breaking something
# deep inside the import mechanism. This is a lot simpler, to say the least.
original_import = __import__
builtins.__import__ = drunk_import
drink()

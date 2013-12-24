from __future__ import print_function
import time

try:
    import builtins
except ImportError:
    import __builtin__ as builtins


def drunk_import(name, *args, **kwargs):
    if name == __name__:
        drink()
    return original_import(name, *args, **kwargs)

def drink(state={'count':0,'start':time.time()}):
    state['count'] += 1
    count = state['count']
    dt = time.time() - state['start']
    bac = ebac(state['count'], dt)
    print('woohoo', state['count'], bac)
    if 0.129 < bac < 0.138:
        print('bullseye')

def ebac(drinks, dt=0, weight=80, metabolism=0.017, water_ratio=0.58):
    return (0.806 * drinks * 1.2) /  (weight * water_ratio) - metabolism * dt

original_import = __import__
builtins.__import__ = drunk_import
drink()

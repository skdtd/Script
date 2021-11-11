import pkgutil
import importlib
import inspect

import bar


list = []
for path, name, ispkg in pkgutil.walk_packages(bar.__path__, prefix='%s.' % bar.__name__):
    if not ispkg:
        m = importlib.import_module(name)
        
        for k, v in inspect.getmembers(m, inspect.isclass):
            if k.startswith('Q'): continue
            print(type(v))
"""
This is the main routes file where we import other application routes
"""
import re
import glob

from app.utils import import_by_path


routes = []
files = glob.glob('*/routes.py')
VARS = [f + '/routes' for f in files]

for var in VARS:
    try:
        routes += import_by_path(re.sub('/', '.', re.sub('.py', '', var)), silent=True)
    except TypeError:
        continue

# example route it should be removed after the core is developed


# end example route

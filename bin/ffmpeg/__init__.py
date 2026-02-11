import os
import sys

cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.relpath(os.path.join(cwd)))
sys.path.append(os.path.relpath(os.path.join(cwd, 'bin')))

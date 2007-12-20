
from pyshin.command import Command
from pyshin.option import Option
h = Option('h')
w = Option('w')
v = Option('v')

cmd1 = Command('cmd1', lambda: 'run with default')

from pyshin.command import Command
from pyshin.option import Option
h = Option('h', '-h')
w = Option('w', '-w')
v = Option('v', '-v')

cmd1 = Command('cmd1', lambda: 'run with default')
  
class CommandWithoutOption(Command):
  pass
  
class TestCommand(Command):
  o = Option('o', '-o')
  a = Option('a', '-a', action='store_true')
  b = Option('b', '-b', action='store_false', dest="bb")
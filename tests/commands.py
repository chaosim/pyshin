
from pyshin.command import Command
from pyshin.option import Option
h = Option('h', '-h')
w = Option('w', '-w')
v = Option('v', '-v')

cmd1 = Command('cmd1', lambda: 'run with default')
  
class CommandWithoutOption(Command):
  pass
  
class TestCommand(Command):
  o = Option('o', '-o', action='store_true')
  a = Option('a', '-a', action='store_true')
  b = Option('b', '-b', action='store_false', dest="bb")  
  c = Option('c', '-c', action='store_const', dest="const_of_c", const='const_in_c_option_of_TestCommand')  
  v = Option('v', '-v', action='store')
  
class Command1(Command):
  value = 1
  result = 0
  def execute(self):
    print 4454, self.command.__name__
    self.result.append(self.value)

class Command2(Command1):
  value = 2
  
class Command3(Command2):
  value = 3
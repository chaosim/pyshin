
from pyshin.command import Command
from pyshin.option import Option
h = Option('-h')
w = Option('-w')
v = Option('-v')

class CommandWithoutOption(Command):
  pass
commandWithoutOption = CommandWithoutOption() 

class TestCommandBase(Command):
  o = Option('-o', action='store_true')
  a = Option('-a', action='store_true')
  b = Option('-b', action='store_false', dest="bb")  
 
class TestCommand(TestCommandBase):
  c = Option('-c', action='store_const', dest="const_of_c", const='const_in_c_option_of_TestCommand')  
  v = Option('-v', action='store')
  longopt = Option('--longopt')

testCommand = TestCommand()
  
class Command1(Command):
  value = 1
  result = []
  def action(self):
    print 'command1 is executed.'
command1 = Command1()

class Command2(Command1):
  value = 2
  def action(self):
    print 'command2 is executed.'
command2 = Command2()
  
class Command3(Command2):
  value = 3
  def action(self):
    print 'command3 is executed.'
command3 = Command3()

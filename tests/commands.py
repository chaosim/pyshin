
from pyshin.command import Command
from pyshin.option import Option
h = Option('-h')
w = Option('-w')
v = Option('-v')

global x
x = 30

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

testCommand = TestCommand()
  
class Command1(Command):
  value = 1
  result = []
  def execute(self):
    #print 4454, self.command.__name__
    self.result.append(self.value)
command1 = Command1()

class Command2(Command1):
  value = 2
command2 = Command2()
  
class Command3(Command2):
  value = 3
command3 = Command3()

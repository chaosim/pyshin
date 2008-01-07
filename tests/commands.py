'''materials made for test'''

from pyshin.command import command
from pyshin.option import Option

class HelpCommand(command):
  helptext = 'base command with help support'
  helpoption = Option('-h', '--help')
  x = Option('-x')
  def action(self):
    if self.followOption(self.command.helpoption):
      self.result = self.helptext
    else:
      self.result = 'execute with -x' 
  
class CommandWithoutOption(command):
  pass

class TestCommandBase(command):
  o = Option('-o', action='store_true')
  a = Option('-a', action='store_true')
  b = Option('-b', action='store_false', dest='bb')  
  longopt =  Option('--longopt')
  def action(self):pass
  
class TestCommand(TestCommandBase):
  c = Option('-c', action='store_const', dest="const_of_c", const='const_in_c_option_of_TestCommand')  
  v = Option('-v', action='store')
  u = Option('-u', action='store')
  longopt = Option('--longopt')

class command1(command):
  value = 1
  result = []
  def action(self):
    print self.command.__name__,

class command2(command1):pass

class command3(command2):pass

'''materials made for test'''

from pyshin.command import command
from pyshin.option import Option

##h = Option('-h')
##w = Option('-w')
##v = Option('-v')

class CommandWithoutOption(command):
  pass

class TestCommandBase(command):
  o = Option('-o', action='store_true')
  a = Option('-a', action='store_true')
  b = Option('-b', action='store_false', dest='bb')  
 
class TestCommand(TestCommandBase):
  c = Option('-c', action='store_const', dest="const_of_c", const='const_in_c_option_of_TestCommand')  
  v = Option('-v', action='store')
  longopt = Option('--longopt')
  

class command1(command):
  value = 1
  result = []
  def action(self):
    print self.command.__name__,

class command2(command1):pass

class command3(command2):pass

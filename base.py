import sys
from pyshin.option import Option, OptionContainer
#from call import CommandCall

class Element(object): 
    def __init__(self, __name__, __doc__=''):
        """Create an 'attribute' description
        """
        if not __doc__ and __name__.find(' ') >= 0:
            __doc__ = __name__
            __name__ = None

        self.__name__=__name__
        self.__doc__=__doc__
        # self.__tagged_values = {}

    def getName(self):
        """ Returns the name of the object. """
        return self.__name__

    def getDoc(self):
        """ Returns the documentation for the object. """
        return self.__doc__

class CommandBase(Element):
# should I make all commands have the same class Command?
# just like all the interfaces have the class  InterfaceClass in zope?
# 2007-12-20 12:07 Have had a try before, but I have delete it now.
  '''Prototype (scarecrow) Commands Implementation
  these codes is stolen form zope.interface.interface.py

  description of command
  option: name, default, help item, type:(boolean, choice, text, ...)
  usage text
  an description string
  the number of the arguments 
  allow interpersed arguments or not?
  use which CommandCall Class?
  action: an callable object.
  '''
  def __init__(self):
    pass
    
  def execute(self, *arg, **kw):
    '''any command instance should overload this method'''
    pass
  
  def __call__(self, *arg, **args):
    '''should produce an CommandCall,
    may be overloaded by actual command'''
    result = CommandCall(self)
    #print self.attrs
    try: result.execute = self.attrs['execute']
    except: result.execute = self.execute
    return result

'''How to use Command see the builtin.py
should define the options and argumetns are permitted by the command'''

##class ACommand(Command):
##  option1 = Option('a', boolean)
##  
##  def execute(self):
##    os.chdir(self.path)
  
# Cmd1 should become an instance of Command

# a = Cmd() should produce an instance of CommandCall
# any occurance of 'a' if an instance of CommandCall


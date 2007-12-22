#import sys
#from types import FunctionType
#from error import InvalidCommand
#from base import Element, fromFunction

from pyshin.option import Option

class Command(object):
  '''  description of command
  option: name, default, help item, type:(boolean, choice, text, ...)
  usage text
  an description string
  the number of the arguments 
  allow interpersed arguments or not?
  use which CommandCall Class?
  action: an callable object.
  '''
  def __init__(self, name=None):
##    if name is None:
##      name = self.__class__.__name__
    #Element.__init__(self, name, __doc__)    
    self._processAttributes()
  
  def _processAttributes(self):
    '''add options, method and data attributes in the command to the call'''
    self.options = {}
    self.dataAttributes = {}
    self.cmdcallMethods = {}
    self._processClassAttributes(self.__class__)
    
  def _processClassAttributes(self, cls):
    
    def Base__dict__(cls, d=None):
      if d is None:
        d = {}
      for c in cls.__bases__:
        Base__dict__(c, d)
      d.update(cls.__dict__)
      return d
        
    from types import FunctionType #UnboundMethodType, 
    for c in cls.__bases__:
      self._processClassAttributes(c)
    for attr, value in cls.__dict__.items():
      if (attr in Base__dict__(Command) and 
          attr not in ['execute']):#'__init__', '__call__', '__repr__' 
        continue
      if isinstance(value, Option):
        self.options[attr]=value
      elif type(value)==FunctionType:
        self.cmdcallMethods[attr] = value
      else: 
        self.dataAttributes[attr] = value

  def execute(self ):# Maybe I should disable arguments to execute , *arg, **kw
    '''any command instance should overload this method'''
  
  def __call__(self): #, *arg, **args
    '''should produce an CommandCall,
    may be overloaded by actual command'''
    
    from call import CommandCall
    cmdcall = CommandCall(self)
    for attr, value in self.cmdcallMethods.items():
      setattr(cmdcall, attr, bind(value, cmdcall)) 
    for attr, value in self.dataAttributes.items():
      setattr(cmdcall, attr, value)
    return cmdcall
  
  def __repr__(self):
    return self.__name__

def rebind(method, obj):
  import new
  return new.instancemethod(method.im_func, obj, obj.__class__)
  
def bind(func, obj):
  import new
  return new.instancemethod(func, obj, obj.__class__)
  

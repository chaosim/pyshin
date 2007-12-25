import sys
#from types import FunctionType
#from error import InvalidCommand
from base import Element#, fromFunction

from pyshin.option import Option

class CommandClass(Element):
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
  def __init__(self, name, bases=(), attrs=None, __doc__=None, __module__=None):
    from pyshin.option import Option#, OptionContainer
    if attrs is None: attrs = {}
    
    if __module__ is None:
      __module__ = attrs.get('__module__')
      if isinstance(__module__, str):
        del attrs['__module__']
      else:
        try: __module__ = sys._getframe(1).f_globals['__name__']
        except (AttributeError, KeyError): pass
    self.__module__ = __module__
  
    d = attrs.get('__doc__')
    if d is not None:
      if __doc__ is None: __doc__ = d
      del attrs['__doc__']
    if __doc__ is None: __doc__ = ''
  
    Element.__init__(self, name, __doc__)
  
    for base in bases:
      if not isinstance(base, CommandClass):
          raise TypeError('Expected base commnds')
    self.bases = bases
    
    self.attrs = attrs
    
    self.options = {}
    self.dataAttributes = {}
    self.cmdcallMethods = {}
    self._processAttributes()
    
    self.__identifier__ = "%s.%s" % (self.__module__, self.__name__)

  def _processAttributes(self, dest=None):
    '''add options, method and data attributes in the command to the call'''    
    from types import FunctionType #UnboundMethodType, 
    if dest is None: dest = self
    for cmd in self.bases:
      cmd._processAttributes(dest)
    for attr, value in self.attrs.items():
      #print attr, value
      if isinstance(value, Option):
        dest.options[attr]=value
      elif type(value)==FunctionType:
        dest.cmdcallMethods[attr] = value
      else: 
        dest.dataAttributes[attr] = value
  
  def allBases(self):
    '''all of the base command except self, by the direction frm self to super base'''
    result = list(self.bases)
    for base in self.bases:
      result += base.allBases()
    return result
  
  def _getattr(self, attr):
    ''' the order of search: self.__dict__, super(CommandClass,self).__getattr__, 
    self.attrs, bases.attrs'''
    try: return self.__dict__ [attr]
    except:
      try: super(CommandClass,self).__getattr__(attr)
      except:
        for cmd in [self]+self.allBases():
          try: return cmd.attrs[attr]
          except: pass
      raise AttributeError, attr
  def __getattr__(self, attr):
    try: return self._getattr(attr)
    except: 
      cmdcall = self()
      return getattr(cmdcall, attr)      
  
  def execute(self):
    '''any command instance should overload this method'''

  def __call__(self, *arg, **kw):
    '''should produce an CommandCall,
    may be overloaded by actual command'''
    from call import CommandCall
    from copy import deepcopy
    cmdcall = CommandCall(self)
    for attr, value in self.cmdcallMethods.items():
      setattr(cmdcall, attr, bind(value, cmdcall)) 
    for attr, value in self.dataAttributes.items():
      setattr(cmdcall, attr, deepcopy(value))
    #print 'asdfdafadf, cmdcall.__dict__', cmdcall.__dict__
    try: 
      cmdcall.__dict__['call'](*arg, **kw)
    except:pass
    return cmdcall
  
  def __mod__(self, arg):
    cmdcall = self()
    cmdcall.arguments.append(arg)
    return cmdcall
  
  def __eq__(self, other):
    return self.__name__==other.__name__

# ------------------------------------------------------------------------------
# process Command Call Chain operator: > < |
  def __rshift__(self, other):
    '''cmda >> cmdb
    produce CommandCallChain to implement pipeline'''
    if isinstance(other, CommandClass): 
      othercall = other()
    return self()>>othercall
##  def __or__(self, other):
##    '''cmda | cmdb
##    produce CommandCallChain to implement pipeline'''
##  __or__ = __rshift__

  def __lshift__(self, other):
    '''cmda < cmdb
    produce CommandCallChain to implement pipeline'''
    if isinstance(other, CommandClass): 
      othercall = other()
    return self()<<othercall
  def __sub__(self, other):
    '''cmd -o'''
    selfcall = self()
    return selfcall-other
  def __gt__(self, other):
    '''cmd >run to execute self'''
    from pyshin.error import InvalidCommand
    from pyshin.call import run
    if other is not run:
      raise InvalidCommand
    return run(self)
  
  def __repr__(self):
    return self.__name__
  
command = CommandClass('Command')

def rebind(method, obj):
  import new
  return new.instancemethod(method.im_func, obj, obj.__class__)
  
def bind(func, obj):
  import new
  return new.instancemethod(func, obj, obj.__class__)
  

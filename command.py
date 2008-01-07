import sys
from base import Element

from pyshin.option import Option

class CommandClass(Element):
  '''Prototype (scarecrow) Commands Implementation
  these codes is from zope.interface.interface.py

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
    from types import FunctionType 
    if dest is None: dest = self
    for cmd in self.bases:
      cmd._processAttributes(dest)
    for attr, value in self.attrs.items():
      if isinstance(value, Option):
        dest.options[attr]=value
        value.name = attr
        setattr(dest, attr, value)
      elif type(value)==FunctionType:
        dest.cmdcallMethods[attr] = value
      else: 
        dest.dataAttributes[attr] = value
  
  def hasOption(self, opt):
    for _, option in self.options.items():
      if opt==option: return True
    return False
  
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
    try: 
      cmdcall.__dict__['call'](*arg, **kw)
    except:pass
    return cmdcall
  
  def __mod__(self, arg):
    '''cmd%arg provide arguments for call on the command''' 
    return self()%arg
  
  def __eq__(self, other):
    return self.__name__==other.__name__

# ------------------------------------------------------------------------------
# process Command Call Chain operator: >> <<
  def __rshift__(self, other):
    '''cmda >> cmdb
    produce CommandCallChain to implement pipeline'''
    if isinstance(other, CommandClass): 
      othercall = other()
    return self()>>othercall

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
    return run(self())
  
  def repr(self): 
    '''__repr__ is used for executing, this replaces standard __repr__'''
    return self.__name__
  
  def __repr__(self):
    '''execute the command'''
    return repr(self())
  
command = CommandClass('Command')

class _sampleCommand(command):
  option1 = Option('-h', '--help')
  option2 = Option('-v', '--verbose')


def rebind(method, obj):
  import new
  return new.instancemethod(method.im_func, obj, obj.__class__)
  
def bind(func, obj):
  import new
  return new.instancemethod(func, obj, obj.__class__)

import __builtin__

class importer:
  '''produce variable in globals() for all options when import command'''
  def __init__(self, globals):
    self.realImport = __builtin__.__import__
    __builtin__.__import__ = self._import
    self.globl = globals
    self.options = {}
      
  def _import(self, name, globals=None, locals=None, fromlist=[]):
    '''produce variable in globals() when import command'''
    result = apply(self.realImport, (name, globals, locals, fromlist))
    if fromlist is not None:
      if fromlist[0]!='*': # from ... import *
        objlist = [getattr(result, x) for x in fromlist]
      else: # from ... import cmd1,cmd2
        objlist = [value for name, value in result.__dict__.items()]  
      for obj in objlist:
        if isinstance(obj, CommandClass): # any obj which is a command
          self.addCommand(obj)
    return result

  def addCommand(self, cmd):
    '''produce variable in globals() for all options in the command'''
    for name, opt in cmd.options.items():
      self.addOption(opt)  

  def addOption(self, cmd, option):
    '''produce variable in globals() for the option'''
    from pyshin.option import ShortOptionOccur, LongOptionOccur
    for opt in [opt[1:] for opt in option._short_opts]:
      if opt not in self.options:
        self.globl[opt] = ShortOptionOccur(option)
      else: self.globl[opt].addCommandOption(cmd, option)
    for opt in [opt[2:] for opt in option._long_opts]:
      if opt not in self.options:
        self.globl[opt] = LongOptionOccur(option)
      else: self.globl[opt].addCommandOption(cmd, option)
  
  def uninstall(self):
    '''restore the __builtin__.__import__'''
    __builtin__.__import__ = self.realImport
  
  def __del__(self):
    '''restore the __builtin__.__import__'''
    __builtin__.__import__ = self.realImport

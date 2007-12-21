import sys
from types import FunctionType
from error import InvalidCommand
from base import Element, fromFunction


_decorator_non_return = object()

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
    from pyshin.option import Option, OptionContainer
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
##        if not isinstance(d, Attribute):
            if __doc__ is None:
                __doc__ = d
            del attrs['__doc__']
    if __doc__ is None: __doc__ = ''
  
    Element.__init__(self, name, __doc__)
  
    for base in bases:
      if not isinstance(base, CommandClass):
          raise TypeError('Expected base commnds')

    self.options = {}
    for name, attr in attrs.items():
      if isinstance(attr, Option):
        attr.command = self
        if not attr.__name__: attr.__name__ = name
        self.options[name] = attr
      elif isinstance(attr, FunctionType):
        attrs[name] = attr #fromFunction(attr, self, name=name)
      elif attr is _decorator_non_return:
        del attrs[name]
##      else:
##        raise InvalidCommand("Concrete attribute, " + name)

    self.attrs = attrs
    self.__identifier__ = "%s.%s" % (self.__module__, self.__name__)

  def execute(self, *arg, **kw):
    '''any command instance should overload this method'''
    pass
  
  def __call__(self, *arg, **args):
    '''should produce an CommandCall,
    may be overloaded by actual command'''
    def bind(func, obj):
     import new
     return new.instancemethod(func, obj, obj.__class__)
    
    from call import CommandCall
    result = CommandCall(self)
    #print self.attrs
    try:
##      print 341423143, self.attrs['execute'] 
      result.execute = bind(self.attrs['execute'], result)
##      print 123443, result.execute 
    except: 
##      print 7768
      result.execute = self.execute
    return result

Command = CommandClass('Command')

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
'''process calls on the commands, produce pipelines, execute the command with 
options and arguments provided'''

##def nameerror():
##  try:
##    a/b
##  except:pass
##  print 234324
##  
##nameerror()  
##stop

from pyshin.option import Option, OptionContainer
from base import CommandBase

class Command(CommandBase):
  '''an occurence of a command
  To implement pipeline, should have result in its instance.
  This class should contain the command it bases on.
  >>> cmd
  >>> cmd -o
  >>> cmd --help
  >>> cd.pyshin.test
  >>> edit.readme.txt
  '''  
  def __init__(self):
    super(Command,self).__init__()

# --------------------------------------------------------------------
# provide option and arguments by operator:
#  -o --option -o(arg) -o==adsfdsf --option==asdfas 
# (option=value) (argvalue)
# cmd.some.value open.readme.txt
# cmd.option.afddsf
# cmd.option==asdfsdakj
  def __sub__(self, other):
    '''an actual option is added to the option set.
    legality of the option should be checked according to class the call based.
     >>> cmd -h
     >>> cmd --help
     >>> cmd --file=='readme.txt'
     '''
    self.options.addOption(other)
    return self

  # maybe it shouldn't put here, maybe in class Option.
  def xxx__neg__(self):
    '''for long option'''
    return x

## DOS/Windows style option dir/h/w, pause implementing this feature.
  def xxx__div__(self, other):
    self.options.add(other)
    return self
  
  def __eq__(self, other):
    '''a value should be assigned to previous option
    validity of the value to the option should be checked.
    >>> cmd --opt==asdf
    '''
    self.validateOptionValue(self.activeoption)
    self.options[self.activeoption] = other
  
  def __call__(self, *arg, **kw):
    '''one or more actual arguments should be added.'''
    #print '__call__'
    if self.call:
      return self.call(*arg, **kw)
    else: return self.execute(*arg, **kw)
  
  
  def __getattr__(self, attr):
    '''maybe set argumets for the command call, it's up to the command of the call'''
    # process class method
    if attr in self.__class__.__dict__: 
      return self.__class__.__dict__[attr]
    
    # default attributes in the instances
    # path.to.here
    # verbose.yes
    
    elif attr in self.__dict__:
      return self.__dict__[attr]
    else: raise AttributeError, attr
  
  def xxx__coerce__(self, other):
    '''prevent errors raising by __getattr__ and __or__'''
    return self,other
  
# ------------------------------------------------------------------------------
# process Command Call Chain operator: > < |
  def __gt__(self, other):
    '''cmda > cmdb
    produce CommandCallChain to implement pipeline'''
    other.input = self.output
    return CommandCallChain([self, other])

  def __lt__(self, other):
    '''cmda < cmdb
    produce CommandCallChain to implement pipeline'''
    return CommandCallChain([self, other])
    
  def __or__(self, other):
    '''cmda | cmdb
    produce CommandCallChain to implement pipeline'''
    return CommandCallChain([self, other])

  def XXX__nonzero__(self):
    '''necessary for cmda and cmdb behaving like a command sequence
    XXX can't do this, for __and__ simulating & operator
    '''
    return 0
  
  def XXX__and__(self, other):
    '''produce CommandCallChain 
    XXX can't do this, for __and__ simulating & operator'''
    return CommandCallChain([self, other])
      
# ------------------------------------------------------------------------------
# trig the execute of the call of the command
  def xxx_execute(self, *arg, **kw):    
    '''the call of the command shouldn't know how to execute itself, this task should
    be dispatch to the command'''
     
    #print 'execute', self.options
    
    result = 'run with'
    if v in self.options:
      result = 'run with more verbose and tab = 4'
      if w in self.options:
        result += ' and tab = 4'
    elif w in self.options:
      result += ' with tab = 4'
    else:
      result += 'default'
    if h in self.options:
      result = '''  usage: cmd1 options .file==name .path==path
  options: 
  -v, --verbose: display verbose information
  -w: set tabwidth to 4
  /h, /help, -h, --help: display this help infomation'''
    return result
  
  def __repr__(self):
    '''all given option and arguments have been given just now,
    should execute the actual action of the command with them, 
    maybe print or don't print the result.'''
    return self.execute()

  def __str__(self):
    '''the CommandCall should be executed according to its command with given option and arguments and print the result.'''  
  __str__ = __repr__

class SingleCommand(Command):
  '''single call of a command'''
        
class CommandChain(Command):
  '''Calls chain of commands.'''
  def __init__(self, calls=None):
    if calls is None:
      self.calls = []
    else: self.calls = calls[:]
     
  def __iter__(self):
    return iter(self.calls)
  
  def __getitem__(self,index):
    return self.calls[index]
  
  def __gt__(self, other):
    '''process things relating to pipeline'''
    other.input = self.calls[-1].output
    self.calls.append(other)
    return self

  def __lt__(self, other):
    '''process things relating to pipeline'''
    self.calls[-1].input = other.output
    self.calls.append(other)
    return self

  __or__ = __gt__

  def xxx__and__(self, other):
    '''produce CommandCallChain 
    XXX can't do this, for __and__ simulating & operator'''
    self.calls.append(other)
  
  def execute(self):
    for call in self.calls[:-1]:
      call.execute()
    self.calls[-1].execute()  
    self.result = self.calls[-1].result
            
# ------------------------------------------------------------------------------
# trig the execute of the call of the command
  def __repr__(self):
    '''all the CommandCall in the chain should be executed with their option and arguments.'''
    return self.execute()
  
  __str__ = __repr__
  
##  def __str__(self):
##    '''all the CommandCall in the chain should be executed with their option and arguments and return the last result.'''
##    #print '__str__'
##    return self.__repr__()

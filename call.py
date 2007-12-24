'''process calls on the commands, produce pipelines, execute the command with 
options and arguments provided'''

from pyshin.option import Option, OptionContainer
from pyshin.error import RepeatOptionError, InvalidOption


class CommandCallBase(object):
  ''' trig the execution by repr(and str? )
  '''  
  def __init__(self):
    self.executed = False

# ------------------------------------------------------------------------------
# trig the execute of the call of the command
  def execute(self):    
    '''the call of the command shouldn't know how to execute itself, this task should
    be dispatch to the command'''
    self.executed = True
   
  def __repr__(self):
    '''all given option and arguments have been given just now,
    should execute the actual action of the command with them, 
    maybe print or don't print the result.'''
    return 'call on %s'%self.command #repr(self.execute()) #wait everythiny is ready

  def __str__(self):
    '''the CommandCall should be executed according to its command with given 
    option and arguments and print the result.'''  
  __str__ = __repr__

class CommandCall(CommandCallBase):
  '''single call of a command
  an occurence of a command
  To implement pipeline, should have result in its instance.
  This class should contain the command it bases on.
  >>> cmd
  >>> cmd -o
  >>> cmd --help
  >>> cd.pyshin.test
  >>> edit.readme.txt'''
  def __init__(self,command):
    super(CommandCall,self).__init__()
    self.command = command
    self.output = None
    self.input = None
    self.options = []

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
    
    if other.name not in self.command.options:
      print 'other.name:', other.name, 'self.command.options', self.command.options
      raise InvalidOption
    if other in self.options:
      raise RepeatOptionError
    from pyshin.option import LongOptionOccur
    from pyshin.error import PyshinSyntaxError
    if isinstance(other, LongOptionOccur) and not other.havePrecededMinus:
      raise PyshinSyntaxError, 'should have two minus before long option'
    self.options.append(other)
    cmdoption = self.command.options[other.name]
    action = cmdoption.action
    if action=='store_true':
      setattr(self, cmdoption.dest, True)
    elif action=='store_false':
      setattr(self, cmdoption.dest, False)
    elif action == "store_const":
      setattr(self, cmdoption.dest, cmdoption.const)
    if action == "store":
      try:
        setattr(self, cmdoption.dest, other.value)
      except:
        self.whoWaitValue = cmdoption.dest
##    elif action == "append":
##      try: 
##        getattr(self, cmdoption.dest).append(other.value)
##      except:
##        setattr(self, cmdoption.dest, [other.value])
##    elif action == "count":
##      try: 
##        x = getattr(self, cmdoption.dest) 
##        x +=  1
##      except:
##        setattr(self, cmdoption.dest, 1)
##    elif action == "callback":
##        args = self.callback_args or ()
##        kwargs = self.callback_kwargs or {}
##        self.callback(self, opt, value, parser, *args, **kwargs)
##    elif action == "help":
##        parser.print_help()
##        parser.exit()
##    elif action == "version":
##        parser.print_version()
##        parser.exit()
##    else:
##        raise RuntimeError, "unknown action %r" % self.action

    return self
  
# pause implementing this feature.
  def xxx__div__(self, other):
    '''DOS/Windows style option dir/h/w'''
  
  def __eq__(self, other):
    '''a value should be assigned to previous option
    validity of the value to the option should be checked.
    >>> cmd --opt==asdf
    '''
    if self.whoWaitValue:
      setattr(self, self.whoWaitValue, other)
      self.whoWaitValue = None
      return self
  
  def __call__(self, *arg, **kw):
    '''one or more actual arguments should be added.'''  
  
  def __getattr__(self, attr):
    '''maybe set argumets for the command call, it's up to the command of the call'''
    if attr in self.__class__.__dict__: 
      return self.__class__.__dict__[attr]
    elif attr in self.__dict__:
      return self.__dict__[attr]
    else: 
      raise AttributeError, attr
  
# ------------------------------------------------------------------------------
# process Command Call Chain operator: > < |
  def __rshift__(self, other):
    '''cmda > cmdb
    produce CommandCallChain to implement pipeline'''
    other.input = self#.output
    return CommandCallChain([self, other])
  def __or__(self, other):
    '''cmda | cmdb
    produce CommandCallChain to implement pipeline'''
  __or__ = __rshift__

  def __lshift__(self, other):
    '''cmda < cmdb
    produce CommandCallChain to implement pipeline'''
    self.input = other#.output
    return CommandCallChain([self, other])

# ------------------------------------------------------------------------------
# trig the execute of the call of the command
  def execute(self):
    if not self.executed:
      if self.input is not None:
        self.input.execute()
      self.action()
      self.executed = True
  
##  def copy(self):
##    cmdcall = self.command()
##    cmdcall.executed = self.executed
##    cmdcall.options = copy(self.options)
##    cmdcall.input = copy(self.input)
##    cmdcall.output = copy(self.output)
          
class CommandCallChain(CommandCallBase):
  '''Calls chain of commands.'''
  def __init__(self, calls=None):
    if calls is None:
      self.calls = []
    else: self.calls = calls[:]
     
  def __iter__(self):
    return iter(self.calls)
  
  def __getitem__(self,index):
    return self.calls[index]
  
  def __rshift__(self, other):
    '''cmd1 > cmd2: pipeline operator'''
    other.input = self.calls[-1]#.output
    self.calls.append(other)
    return self
  
  def __or__(self, other):
    '''cmd1 | cmd2: pipeline operator'''
  __or__ = __rshift__

  def __lshift__(self, other):
    '''cmd1 < cmd2: pipeline operator'''
    #print 4123214, self.calls, other
    self.calls[-1].input = other#.output
    self.calls.append(other)
    
    return self


# ------------------------------------------------------------------------------
# trig the execute of the call of the command
  def execute(self):
    #print self.calls
    for call in self.calls:#[:-1]
      #print call
      call.execute()
    #self.calls[-1].execute() 
    #self.executed = True
    #self.result = self.calls[-1].result

  def __repr__(self):
    '''all the CommandCall in the chain should be executed with their option and 
    arguments and return the repr of the last result'''
    return '%s'%self.calls #repr(self.execute())
  
  def __str__(self):
    '''all the CommandCall in the chain should be executed with their option 
    and arguments and return the str of the last result.'''
  __str__ = __repr__

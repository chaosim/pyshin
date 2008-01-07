'''process calls on the commands, produce pipelines, execute the command with 
options and arguments provided'''

from option import Option
from error import RepeatOptionError, InvalidOption
from command import CommandClass

ExecutingCommand = False

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
   
  def repr(self):
    '''all given option and arguments have been given just now,
    should execute the actual action of the command with them, 
    maybe print or don't print the result.'''
    return 'call on %s'%self.command.repr() #repr(self.execute()) #wait everythiny is ready

  def __repr__(self):
    '''all given option and arguments have been given just now,
    should execute the actual action of the command with them, 
    maybe print or don't print the result.'''
    self.execute()
    return repr(self.result)

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
    self.whoWaitValue = None # the dest of the current option which is absense of value
    self.options = []
    self.arguments = [] # arguments of the CommandCall

# --------------------------------------------------------------------
# provide option and arguments by operator:
#  -o --option -o/arg -o/adsfdsf --option/asdfas 
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
    
    if other.option is not None:
      if not self.command.hasOption(other.option):
        raise InvalidOption
    elif other.name not in self.command.options:
      raise InvalidOption
    if other in self.options:
      raise RepeatOptionError
    from pyshin.option import LongOptionOccur
    from pyshin.error import PyshinSyntaxError
    if isinstance(other, LongOptionOccur) and not other.havePrecededMinus:
      raise PyshinSyntaxError, 'should have two minus before long option'
    self.options.append(other)
   
    # get the arguments after the option
    if 'argForCmdCall' in other.__dict__:
      self.arguments += other.__dict__['argForCmdCall']
    
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

  def __mod__(self, arg):
    self.arguments.append(arg)
    return self

# pause implementing this feature.
  def xxx__div__(self, other):
    '''DOS/Windows style option dir/h/w'''
  
  def __eq__(self, other):
    '''a value should be assigned to previous option
    validity of the value to the option should be checked.
    >>> cmd --opt==asdf
    '''
    return isinstance(other, CommandCall) and self.command==other.command
  
  def __call__(self, *arg, **kw):
    '''one or more actual arguments should be added.'''  
  
  def __getattr__(self, attr):
    '''maybe set argumets for the command call, it's up to the command of the call'''
    if attr in self.__class__.__dict__: 
      return self.__class__.__dict__[attr]
    elif attr in self.__dict__:
      return self.__dict__[attr]
    else: 
      self.saveAttributeArgument(attr)
      return self
  
  def saveAttributeArgument(self, attr):
    raise AttributeError, attr

# ------------------------------------------------------------------------------
# process Command Call Chain operator: >> << |
  def __rshift__(self, other):
    '''cmda >> cmdb
    produce CommandCallChain to implement pipeline'''
    other.input = self
    chain = CommandCallChain([self, other])
    chain.loop = [self, other]
    chain.loopDirection = '>>'
    return chain

  def __lshift__(self, other):
    '''cmda << cmdb
    produce CommandCallChain to implement pipeline'''
    self.input = other#.output
    chain = CommandCallChain([self, other])
    chain.loop = [self, other]
    chain.loopDirection = '<<'
    return chain
  def followOption(self, option):
    print option, self.options
    if option in self.options: 
      return True
    return False
# ------------------------------------------------------------------------------
# trig the execute of the call of the command
  def __gt__(self, other):
    '''cmd >run to execute self'''
    from pyshin.error import InvalidCommand
    from pyshin.call import run
    if other is not run:
      raise InvalidCommand
    return run(self)

  def execute(self):
    global ExecutingCommand
    ExecutingCommand = True
    if not self.executed:
      if self.input is not None:
        self.input.execute()
      self.action()
      self.executed = True
    ExecutingCommand = False
           
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
    '''cmd1 >> cmd2: pipeline operator'''
    from pyshin.error import LoopInCommandCallChain
    if isinstance(other, CommandClass):
      other = other()
    lastcall = self.calls[-1]
    if self.loopDirection=='>>':
      if other in self.loop: 
        raise LoopInCommandCallChain
      self.loop.append(other)
    else: 
      self.loop = [lastcall, other]
      self.loopDirection = '>>'
   
    other.input = lastcall
    self.calls.append(other)
    return self
  
  def __lshift__(self, other):
    '''cmd1 << cmd2: pipeline operator'''
    from pyshin.error import LoopInCommandCallChain
    if isinstance(other, CommandClass):
      other = other()
    lastcall = self.calls[-1]
    if self.loopDirection=='<<':
      if other in self.loop: 
        raise LoopInCommandCallChain
      self.loop.append(other)
    else: 
      self.loop = [lastcall, other]
      self.loopDirection = '<<'
   
    lastcall.input = other
    self.calls.append(other)
    
    return self


# ------------------------------------------------------------------------------
# trig the execute of the call of the command
  def execute(self):
    global ExecutingCommand
    ExecutingCommand = True
    for call in self.calls:
      call.execute()
    ExecutingCommand = False
    self.result = ''
    
  def __gt__(self, other):
    '''cmd >run to execute self'''
    from pyshin.error import InvalidCommand
    from pyshin.call import run
    if other is not run:
      raise InvalidCommand
    return run(self)

  def repr(self):
    '''all the CommandCall in the chain should be executed with their option and 
    arguments and return the repr of the last result'''
    return '%s'%[call.repr() for call in self.calls] #repr(self.execute())
  
  def __repr__(self):
    '''all the CommandCall in the chain should be executed with their option and 
    arguments and return the repr of the last result'''
    self.execute()    
    return self.result
  
  def __str__(self):
    '''all the CommandCall in the chain should be executed with their option 
    and arguments and return the str of the last result.'''
  __str__ = __repr__

class _run:
  def __call__(self, cmd):
    if isinstance(cmd, CommandClass):
      cmd = cmd()
      cmd.execute()
    else:
      cmd.execute()
    #return cmd
run = _run()
'''process calls on the commands, produce pipelines, execute the command with 
options and arguments provided'''

from pyshin.option import Option, OptionContainer
from pyshin.error import RepeatOptionError, InvalidOption


class CommandCallBase(object):
  ''' trig the execution by repr(and str? )
  '''  
  def __init__(self):
    pass

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
      raise InvalidOption
    if other in self.options:
      raise RepeatOptionError
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

# ------------------------------------------------------------------------------
# trig the execute of the call of the command
  def execute(self):
    for call in self.calls[:-1]:
      call.execute()
    self.calls[-1].execute()  
    #self.result = self.calls[-1].result

  def __repr__(self):
    '''all the CommandCall in the chain should be executed with their option and 
    arguments and return the repr of the last result'''
    return '%s'%self.calls #repr(self.execute())
  
  
  def __str__(self):
    '''all the CommandCall in the chain should be executed with their option 
    and arguments and return the str of the last result.'''
  __str__ = __repr__

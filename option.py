from error import OptionError
from base import Attribute

# =========================================================================
# from python24\lib\optparse.py

# Not supplying a default is different from a default of None,
# so we need an explicit "not supplied" value.
NO_DEFAULT = ("NO", "DEFAULT")

from gettext import gettext as _

def _repr(self):
    return "<%s at 0x%x: %s>" % (self.__class__.__name__, id(self), self)

_builtin_cvt = {"int" : (int, _("integer")),
               "long" : (long, _("long integer")),
               "float" : (float, _("floating-point")),
               "complex" : (complex, _("complex")) }
def check_builtin(option, opt, value):
  (cvt, what) = _builtin_cvt[option.type]
  try: return cvt(value)
  except ValueError:
    raise OptionValueError(_("option %s: invalid %s value: %r") % 
           (opt, what, value))

def check_choice(option, opt, value):
  if value in option.choices: return value
  else:
    choices = ", ".join(map(repr, option.choices))
    raise OptionValueError(_("option %s: invalid choice: %r (choose from %s)")
        % (opt, value, choices))

class Option(Attribute):
  """ Instance attributes:
    _short_opts:[string] _long_opts:[string]
    action: string       type: string         dest:string
    default:any          nargs: int            const: any           
    choices: [string]   
    callback:function    callback_args:(any*) callback_kwargs:{string:any}
    help:string          metavar:string
  """

  # instance attributes set through keyword args to the constructor.
  ATTRS = ['action', 'type', 'dest', 'default', 'nargs', 'const', 'choices',
           'callback', 'callback_args', 'callback_kwargs', 'help', 'metavar']

  def __init__(self, *opts, **attrs):
      Attribute.__init__(self, self.__class__.__name__)
      
      self._short_opts = []
      self._long_opts = []
      self._set_opt_strings(opts)

      self._set_attrs(attrs)

      for checker in self.CHECK_METHODS:
          checker(self)

  def _set_opt_strings(self, opts):
      for opt in opts:
          if len(opt) < 2:
              raise OptionError(
                  "invalid option string %r: "
                  "must be at least two characters long" % opt, self)
          elif len(opt) == 2:
              if not (opt[0] == "-" and opt[1] != "-"):
                  raise OptionError( "invalid short option string %r: "
                      "must be of the form -x, (x any non-dash char)" % opt, self)
              self._short_opts.append(opt)
          else:
              if not (opt[0:2] == "--" and opt[2] != "-"):
                  raise OptionError( "invalid long option string %r: "
                      "must start with --, followed by non-dash" % opt, self)
              self._long_opts.append(opt)

  def _set_attrs(self, attrs):
      for attr in self.ATTRS:
          if attrs.has_key(attr):
              setattr(self, attr, attrs[attr])
              del attrs[attr]
          else:
              if attr == 'default': setattr(self, attr, NO_DEFAULT)
              else: setattr(self, attr, None)
      if attrs:
          attrs = attrs.keys()
          attrs.sort()
          raise OptionError( "invalid keyword arguments: %s" % ", ".join(attrs), self)


  # actions allowed by option parsers
  ACTIONS = ("store", "store_const", "store_true", "store_false", "append",
             "count", "callback", "help", "version")

  # -- Constructor validation methods --------------------------------
  def _check_action(self):
      if self.action is None:
          self.action = "store"
      elif self.action not in self.ACTIONS:
          raise OptionError("invalid action: %r" % self.action, self)

  # The set of actions which may consume an argument from the command line.
  TYPED_ACTIONS = ("store", "append", "callback")
  # The set of actions which *require* a value type and always consume an argument from the command line.
  ALWAYS_TYPED_ACTIONS = ("store", "append")
  # known types for option parsers, listed here for argument validation.
  TYPES = ("string", "int", "long", "float", "complex", "choice")

  # Dictionary of argument checking functions, which convert and
  # validate option arguments according to the option type.
  # check(option : Option, opt : string, value : string) -> any
  #   option: the Option instance calling the checker
  #   opt: option seen on the command-line eg. -a, --file
  #   value is the option argument seen on the command-line
  # If no checker is defined for a type, arguments will be
  # unchecked and remain strings.
  TYPE_CHECKER = { "int": check_builtin, "long":check_builtin, "float":check_builtin,
                   "complex":check_builtin, "choice": check_choice}


  def _check_type(self):
      if self.type is None:
          if self.action in self.ALWAYS_TYPED_ACTIONS:
              if self.choices is not None:
                  self.type = "choice"
              else: self.type = "string"
      else:
          if type(self.type) is type:
              self.type = self.type.__name__
          if self.type == "str": self.type = "string"

          if self.type not in self.TYPES: 
            raise OptionError("invalid option type: %r" % self.type, self)
          if self.action not in self.TYPED_ACTIONS:
              raise OptionError( "must not supply a type for action %r" 
                                 % self.action, self)

  def _check_choice(self):
      if self.type == "choice":
          if self.choices is None:
              raise OptionError( "must supply a list of choices for type 'choice'", self)
          elif type(self.choices) not in (types.TupleType, types.ListType):
              raise OptionError( "choices must be a list of strings ('%s' supplied)"
                  % str(type(self.choices)).split("'")[1], self)
      elif self.choices is not None:
          raise OptionError( "must not supply choices for type %r" % self.type, self)

  #  if the action is one of these, there must be a destination
  STORE_ACTIONS = ("store", "store_const", "store_true", "store_false", "append", "count")

  def _check_dest(self):
    takes_value = (self.action in self.STORE_ACTIONS or self.type is not None)
    if self.dest is None and takes_value:
      if self._long_opts:
          # eg. "--foo-bar" -> "foo_bar"
          self.dest = self._long_opts[0][2:].replace('-', '_')
      else:
          self.dest = self._short_opts[0][1]

  def _check_const(self):
      if self.action != "store_const" and self.const is not None:
          raise OptionError(
              "'const' must not be supplied for action %r" % self.action,
              self)

  def _check_nargs(self):
      if self.action in self.TYPED_ACTIONS:
          if self.nargs is None:
              self.nargs = 1
      elif self.nargs is not None:
          raise OptionError(
              "'nargs' must not be supplied for action %r" % self.action,
              self)

  def _check_callback(self):
      if self.action == "callback":
          if not callable(self.callback):
              raise OptionError(
                  "callback not callable: %r" % self.callback, self)
          if (self.callback_args is not None and
              type(self.callback_args) is not types.TupleType):
              raise OptionError(
                  "callback_args, if supplied, must be a tuple: not %r"
                  % self.callback_args, self)
          if (self.callback_kwargs is not None and
              type(self.callback_kwargs) is not types.DictType):
              raise OptionError(
                  "callback_kwargs, if supplied, must be a dict: not %r"
                  % self.callback_kwargs, self)
      else:
          if self.callback is not None:
              raise OptionError(
                  "callback supplied (%r) for non-callback option"
                  % self.callback, self)
          if self.callback_args is not None:
              raise OptionError(
                  "callback_args supplied for non-callback option", self)
          if self.callback_kwargs is not None:
              raise OptionError(
                  "callback_kwargs supplied for non-callback option", self)


  CHECK_METHODS = [_check_action, _check_type, _check_choice, _check_dest, 
          _check_const, _check_nargs, _check_callback]

  def __eq__(self, other):
    return (self.__class__==other.__class__ and 
            self._short_opts==other._short_opts and
            self._long_opts==other._long_opts)
            
  # -- Miscellaneous methods -----------------------------------------

  def __str__(self):
      return "/".join(self._short_opts + self._long_opts)
  __repr__ = _repr

  def takes_value(self):
      return self.type is not None

  def get_opt_string(self):
      if self._long_opts: return self._long_opts[0]
      else: return self._short_opts[0]


  # -- Processing methods --------------------------------------------
  def check_value(self, opt, value):
      checker = self.TYPE_CHECKER.get(self.type)
      if checker is None: return value
      else: return checker(self, opt, value)

  def convert_value(self, opt, value):
    if value is not None:
      if self.nargs == 1:
        return self.check_value(opt, value)
      else:
        return tuple([self.check_value(opt, v) for v in value])

  def process(self, opt, value, values, parser):
    value = self.convert_value(opt, value)
    return self.take_action(self.action, self.dest, opt, value, values, parser)

  def take_action(self, action, dest, opt, value, values, parser):
    if action == "store": setattr(values, dest, value)
    elif action == "store_const": setattr(values, dest, self.const)
    elif action == "store_true": setattr(values, dest, True)
    elif action == "store_false": setattr(values, dest, False)
    elif action == "append": values.ensure_value(dest, []).append(value)
    elif action == "count": setattr(values, dest, values.ensure_value(dest, 0) + 1)
    elif action == "callback":
      args = self.callback_args or ()
      kwargs = self.callback_kwargs or {}
      self.callback(self, opt, value, parser, *args, **kwargs)
    elif action == "help":
      parser.print_help()
      parser.exit()
    elif action == "version":
      parser.print_version()
      parser.exit()
    else:
      raise RuntimeError, "unknown action %r" % self.action
    return 1
  
  def needValue(self):
    return self.action in ['store', 'append', 'count']


    
from pyshin.error import OptionShouldnotHaveValue

class OptionOccur(object):
  '''Occurence of Option in the CommandCall
  出现在命令调用中的选项'''
  def __init__(self, command=None, option=None):
    self.cmdOpts = [(command, option)]
    
  def addCommandOption(command, option):
    self.commandOptions.append((command, option))
  
  def __call__(self, value):
    '''should not give value to option like -o(arg), (*arg, **kw) only 
    reserved for command
    '''
    from pyshin.error import PyshinSyntaxError
    raise PyshinSyntaxError
##    if self.option.needValue():
##      self.value = value
##    else: raise OptionShouldnotHaveValue
##    return self
  
  def __neg__(self):
    '''for long option --opt'''
  
  def __eq__(self, other):
    '''should not use == to set value for option, use / instead '''
    from call import ExecutingCommand
    if ExecutingCommand:      
      #print self._short_opts, self._long_opts
      print self, other
      if type(other)==type('-o'):
        if other in self.option._short_opts or other in self.option._long_opts:
          return True
      else: 
        print other
        return self._short_opts==other._short_opts and self._long_opts==other._long_opts
    else:
      from pyshin.error import PyshinSyntaxError
      raise PyshinSyntaxError
  
  def __mod__(self, other):
    '''%arg provide argument for the CommandCall through the option'''
    if 'argForCmdCall' in self.__dict__:
      self.__dict__['argForCmdCall'].append(other)
    else: self.__dict__['argForCmdCall'] = [other]
    return self
    
  def __div__(self, other):
    '''use / to provide value for the option '''
    from pyshin.error import OptionWithTooManySlash
    if self.option.needValue():
      #print 253452535, other, self.__dict__
      if 'value' in self.__dict__: 
        raise OptionWithTooManySlash
      else:
        self.value = other
    else: raise OptionShouldnotHaveValue
    return self
  
  def __getattr__(self, attr):
    from call import ExecutingCommand
    if ExecutingCommand:
        return self.__dict__[attr]
    else:
      if attr=='value': 
          return self.__dict__[attr]
      try:
        return self.__dict__[attr]
      except:
        if not self.option.needValue():        
          raise OptionShouldnotHaveValue
        try: 
          self.__dict__['value'] +='.'+attr
        except:
          self.__dict__['value'] = attr
        return self
  
  def __repr__(self):
    return '-%s'%self.name   
  __str__ = __repr__

class ShortOptionOccur(OptionOccur):
  def __neg__(self):
    '''prevent --o'''
    from pyshin.error import ShouldBeShortOption
    raise ShouldBeShortOption, self
    
class LongOptionOccur(OptionOccur):
  def __init__(self, name, option=None):
    super(self.__class__, self).__init__(name, option)
    self.havePrecededMinus = False
    
  def __neg__(self):
    '''used for second minus in --opt'''
    if not self.havePrecededMinus:
      self.havePrecededMinus = True
      return self
    else:
      from pyshin.error import PyshinSyntaxError
      raise PyshinSyntaxError, self
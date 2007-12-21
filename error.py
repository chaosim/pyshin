class PyshinError(Exception):
  pass

class InvalidCommand(PyshinError):
  pass
  
class InvalidOption(PyshinError):
  pass
  
class PyshinSyntaxError(PyshinError):
  '''syntax error in pyshin command
  pyshin命令语法错误
  '''
  pass

class RepeatOptionError(PyshinSyntaxError):pass

class OutofRange(PyshinError):
  '''value provided is out of range
  值超出范围'''
  pass  

class WrongValueType(PyshinError):
  '''the type of value is wrong
  值类型错误'''
  pass
  
class WrongOption:
  '''wrong option
  错误选项'''
  pass
  
class TooManyArgumnet(PyshinError):
  '''too many arguments
  参数太多'''
  pass
  
class TooFewArgumnet(PyshinError):
  '''too few arguments
  参数太少'''
  pass

class OptParseError (Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class OptionError (OptParseError):
    """
    Raised if an Option instance is created with invalid or
    inconsistent arguments.
    """

    def __init__(self, msg, option):
        self.msg = msg
        self.option_id = str(option)

    def __str__(self):
        if self.option_id:
            return "option %s: %s" % (self.option_id, self.msg)
        else:
            return self.msg

class OptionConflictError (OptionError):
    """
    Raised if conflicting options are added to an OptionParser.
    """

class OptionValueError (OptParseError):
    """
    Raised if an invalid option value is encountered on the command
    line.
    """

class BadOptionError (OptParseError):
    """
    Raised if an invalid or ambiguous option is seen on the command-line.
    """



import unittest

from zope.testing.doctestunit import DocTestSuite, DocFileSuite
from zope.testing import doctest

import exceptions

from pyshin.command import command
from pyshin.call import CommandCall, CommandCallChain
from pyshin.option import Option, OptionOccur, ShortOptionOccur
from pyshin.error import RepeatOptionError, InvalidOption

from pyshin.tests.commands import TestCommand

class CommandCallTestCase(unittest.TestCase):

  def setUp(self):
    pass
      
  def xxxtest_CommandCall(self):
    # xxx wait some other done correctly.
    cmda = CommandCall('a')
    cmdb = CommandCall('b')                
    self.assertRaises(exceptions.TypeError, repr, cmda) #???
  
  def test_pipeline_operator(self):
    '''Pipeline operators | > < should produce CommandCallChain'''
    # a | b
    cmda = CommandCall('a')
    cmdb = CommandCall('b')                
    result = cmda | cmdb
    self.assert_(isinstance(result, CommandCallChain))
    self.assert_((result[0] is cmda) and (result[1] is cmdb))
    # a >> b 
    result =cmda >> cmdb
    self.assert_(isinstance(result, CommandCallChain))
    self.assert_((result[0] is cmda) and (result[1] is cmdb))
    # a << b 
    result = cmda << cmdb
    self.assert_(isinstance(result, CommandCallChain))
    self.assert_((result[0] is cmda) and (result[1] is cmdb))
    
  def test_forward_pipeline(self):
    '''The output of the previous call become the input of the next call
    前一个命令的输入成为后一个命令的输入'''
    cmda = CommandCall('a')
    cmdb = CommandCall('b')                
    chain = cmda >> cmdb
    self.assert_(cmdb.input is cmda)#.output

  def xxxtest__and__(self):
    result = self.cmda and self.cmdb
    self.assert_(isinstance(result, CommandCallChain))
  
  def test_option(self):
    '''"cmd -o" should add the option o to cmd.options'''
    cmd = CommandCall(TestCommand)
    o = OptionOccur('o')
    result = cmd -o
    self.assert_(o in cmd.options)
  
  def test_no_repeat_option(self):
    '''Meeting with options repeated should raise RepeatOptionError'''
    cmd = CommandCall(TestCommand)
    o = OptionOccur('o')
    try: 
      result = cmd -o -o
      self.fail('should raise syntax error')
    except RepeatOptionError: pass
  
  def test_legal_option(self):
    '''The option followed after Commandcall must be an option of the Command'''
    from pyshin.tests.commands import CommandWithoutOption
    cmd = CommandCall(CommandWithoutOption)
    o = OptionOccur('o')
    try:
      result = cmd -o
      self.fail('should check invalid option')
    except InvalidOption: pass
    cmd = CommandCall(TestCommand)
    u = OptionOccur('u')
    try:
      result = cmd -u
      self.fail('should check invalid option')
    except InvalidOption: pass

  def test_long_short_option(self):
    from pyshin.option import LongOptionOccur, ShortOptionOccur
    from pyshin.error import PyshinSyntaxError
    from pyshin.error import ShouldBeShortOption

    o = ShortOptionOccur('-o')
    try:
      -o      
      self.fail('should check invalid option')
    except ShouldBeShortOption: pass

    longopt = LongOptionOccur('longopt')
    try:
      --longopt      
      self.fail('should check too many minus')
    except PyshinSyntaxError, e: 
      pass

    cmd = CommandCall(TestCommand)
    longopt = LongOptionOccur('longopt')
    try:
      cmd-longopt      
      self.fail('should check too few minus')
    except PyshinSyntaxError, e: 
      pass
    
  def test_addOptionToCommand(self):
    ''' Meeting with options should store value in the Commandcall'''
    a = OptionOccur('a')
    cmd = CommandCall(TestCommand)
    result = cmd -a
    self.assertEqual(result.a, True)  
    
    b = OptionOccur('b')
    cmd = CommandCall(TestCommand)
    result = cmd -b
    self.assertEqual(result.bb, False)  
    
    c = OptionOccur('c')
    cmd = CommandCall(TestCommand)
    result = cmd -c
    self.assertEqual(result.const_of_c, 'const_in_c_option_of_TestCommand')  

    v = OptionOccur('v', TestCommand.options['v'])
    cmd = CommandCall(TestCommand)
##    new>>> should not do this:
##    result = cmd -v('given_value_in__call__')
##    self.assertEqual(result.v, 'given_value_in__call__')  

    v = OptionOccur('v')
    cmd = CommandCall(TestCommand)
    result = cmd -v=='given_value_in__call__'
    self.assertEqual(result.v, 'given_value_in__call__')  

    v = OptionOccur('v', TestCommand.options['v'])
    cmd = CommandCall(TestCommand)
    result = cmd -v.readme.txt
    self.assertEqual(result.v, 'readme.txt')  

  def wait_test_state_of_executed(self):
    '''the state of 'executed' should change after the call is executed.'''
    cmd = TestCommand()
    self.assertEqual(cmd.executed, False)
    cmd.execute()
    self.assertEqual(cmd.executed, True)
    
  def test_attr_arg(self):
    '''dotted name argument

    xxx>>> class _Open(CommandCall):
    ...   """should base on Command class which allow dotted path filename as arguments"""
    ...   def __init__(self):
    ...     super(_Open, self).__init__(None, None)
    ...     self.path = ''
    ...   def __getattr__(self, attr):
    ...     try:
    ...       return super(_Open, self).__getattr__(attr)
    ...     except:
    ...       if self.path=='':
    ...         self.path += attr
    ...       else:
    ...         self.path += '.'+attr
    ...       return self
    
    xxx>>> open = _Open()
    xxx>>> open.readme.txt.path
    'readme.txt'
    '''

class CommandCallChainTestCase(unittest.TestCase):
  def setUp(self):
    pass
      
  def test_executeAllCommandCall(self):
    '''Executing chain should execut every Command in it
    >>> from pyshin.tests.commands import command1, command2
    >>> cmd1 = command1
    >>> cmd2 = command2
    >>> chain = cmd1>>cmd2
    >>> chain.execute()
    command1 command2
    '''
  def wait_test_executeCommandCallAccordingToDirection(self):
    '''Execute commands according the direction of the pipeline
    >>> from pyshin.tests.commands import command1, command2, command3
    >>> cmd1 = command1()
    >>> cmd2 = command2()
    >>> cmd3 = command3()
    >>> chain = cmd1<<cmd2<<cmd3
    
    >>> print chain
    [call on command1, call on command2, call on command3]
    
    >>> chain.execute()
    command3 command2 command1
    
    >>> chain = command1<<command2>>command3
    >>> chain.execute()
    command2 command1 command3
    '''

class OptionTestCase(unittest.TestCase):
  '''test usage of option'''        
  def test_OptionWithoutValue(self):
    '''if the option need no value, should disable __call__, __getattr__ 
    and __eq__'''
    from pyshin.error import OptionShouldnotHaveValue
    opt = Option('-o', action='store_true')
    #print opt.dest
    #opt.dest = None
    o = OptionOccur('-o', opt)
##    try:
##      o('arg') # new>>> should not do this.
##      self.fail('should check ShouldnotHaveValue')
##    except OptionShouldnotHaveValue:
##      pass
    try:
      o.arg
      self.fail('should check ShouldnotHaveValue')
    except OptionShouldnotHaveValue:
      pass
  def test_OptionWithoutValue__eq__(self):
    '''if the option need no value, should disable __call__, __getattr__ 
    and __eq__'''
    from pyshin.error import OptionShouldnotHaveValue
    class cmd(command):
      o = Option('-o', action='store_true')
    #print '54354345 cmd.options', cmd.options
    o = ShortOptionOccur('o', cmd.options['o'])
    try:
      cmd-o=='arg'
      self.fail('should check ShouldnotHaveValue')
    except OptionShouldnotHaveValue:
      pass
  def test_NoValueFrom__call__(self):
    '''option should not take value frome __call__  '''
    from pyshin.error import PyshinSyntaxError
    o = ShortOptionOccur('o')
    self.assertRaises(PyshinSyntaxError, o.__call__, None)
def test_suite():
  suite = unittest.TestSuite((unittest.makeSuite(CommandCallTestCase),
          unittest.makeSuite(CommandCallChainTestCase),
          unittest.makeSuite(OptionTestCase),
          DocTestSuite('pyshin.tests.test_cmdcall', 
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)  
        ))
  return suite

if __name__ == '__main__':
  unittest.main()
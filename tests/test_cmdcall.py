import unittest

from zope.testing.doctestunit import DocTestSuite, DocFileSuite
from zope.testing import doctest

import exceptions

from pyshin.call import CommandCall
from pyshin.call import CommandCallChain
from pyshin.option import Option, OptionOccur
from pyshin.error import RepeatOptionError, InvalidOption

from pyshin.tests.commands import TestCommand

class CommandCallTestCase(unittest.TestCase):

  def setUp(self):
    pass
      
  def xxxtest_CommandCall(self):
    # xxx wait some other done correctly.
    cmda = CommandCall('a')
    cmdb = CommandCall('b')                
    self.assertRaises(exceptions.TypeError, repr, cmda)
  
  def test_pipeline_operator(self):
    '''Pipeline operators | > < should produce CommandCallChain'''
    # a | b
    cmda = CommandCall('a')
    cmdb = CommandCall('b')                
    result = cmda | cmdb
    self.assert_(isinstance(result, CommandCallChain))
    self.assert_((result[0] is cmda) and (result[1] is cmdb))
    # a > b 
    result =cmda > cmdb
    self.assert_(isinstance(result, CommandCallChain))
    self.assert_((result[0] is cmda) and (result[1] is cmdb))
    # a < b 
    result = cmda < cmdb
    self.assert_(isinstance(result, CommandCallChain))
    self.assert_((result[0] is cmda) and (result[1] is cmdb))
    
  def test_forward_pipeline(self):
    '''The output of the previous call become the input of the next call
    前一个命令的输入成为后一个命令的输入'''
    cmda = CommandCall('a')
    cmdb = CommandCall('b')                
    chain = cmda > cmdb
    self.assert_(cmdb.input is cmda.output)

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
    '''The option followed after commandcall must be an option of the Command'''
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

  def xxxtest_long_short_option(self):
    cmd = CommandCall(TestCommand)
    afd = OptionOccur('dsf')
    try:
      result = cmd --afd      
      self.fail('should check invalid option')
    except InvalidOption: pass
    
  def test_addOptionToCommand(self):
    ''' Meeting with options should store value in the commandcall'''
    #print 'begin test_addOptionToCommand'
    a = OptionOccur('a')
    cmd = CommandCall(TestCommand)
    #print 7687786,a
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

    v = OptionOccur('v')
    cmd = CommandCall(TestCommand)
    result = cmd -v('given_value_in__call__')
    self.assertEqual(result.v, 'given_value_in__call__')  

    v = OptionOccur('v')
    cmd = CommandCall(TestCommand)
    #v.value = 'given_value_in__call__'
    result = cmd -v=='given_value_in__call__'
    self.assertEqual(result.v, 'given_value_in__call__')  

    v = OptionOccur('v')
    cmd = CommandCall(TestCommand)
    result = cmd -v.readme.txt
    self.assertEqual(result.v, 'readme.txt')  

  def test_attr_arg(self):
    '''dotted name argument

    >>> class _Open(CommandCall):
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
    
    >>> open = _Open()
    >>> open.readme.txt.path
    'readme.txt'
    '''

class CommandCallChainTestCase(unittest.TestCase):
  def setUp(self):
    pass
      
  def test_executeAllCommandCall(self):
    '''Executing chain should execut every command in it'''
    from pyshin.tests.commands import Command1, Command2, Command3
    result = []
    cmd1 = Command1()
    cmd2 = Command2()
    cmd3 = Command3()
    cmd1.execute()
    print result
    chain = cmd1>cmd2>cmd3
    print chain.calls
    chain.execute()
    self.assertEqual(result, [1,2,3])
        
def test_suite():
  suite = unittest.TestSuite((unittest.makeSuite(CommandCallTestCase),
          unittest.makeSuite(CommandCallChainTestCase)
          #DocTestSuite('pyshin.tests.test_command'),  
         ))
  return suite

if __name__ == '__main__':
  unittest.main()
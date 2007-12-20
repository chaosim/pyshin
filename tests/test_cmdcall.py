import unittest

from zope.testing.doctestunit import DocTestSuite, DocFileSuite
from zope.testing import doctest

import exceptions

from pyshin.command import CommandCall
from pyshin.call import CommandCallChain
from pyshin.option import Option

class CommandTestCase(unittest.TestCase):

  def setUp(self):
    self.cmda = CommandCall('a', None)
    self.cmdb = CommandCall('b', None)                
      
  def xxxtest_Command(self):
    # xxx wait some other done correctly.
    self.assertRaises(exceptions.TypeError, repr, self.cmda)
  
  def test_operator(self):
    '''pipeline operator'''
    # a | b
    result = self.cmda | self.cmdb
    self.assert_(isinstance(result, CommandCallChain))
    self.assert_((result[0] is self.cmda) and (result[1] is self.cmdb))
    # a > b 
    result = self.cmda > self.cmdb
    self.assert_(isinstance(result, CommandCallChain))
    self.assert_((result[0] is self.cmda) and (result[1] is self.cmdb))
    # a < b 
    result = self.cmda<self.cmdb
    self.assert_(isinstance(result, CommandCallChain))
    self.assert_((result[0] is self.cmda) and (result[1] is self.cmdb))
    
  def test_forward_pipeline(self):
    '''the output of the previous call become the input of next call
    前一个命令的输入成为后一个命令的输入'''
    chain = self.cmda > self.cmdb
    self.assert_(self.cmdb.input is self.cmda.output)

  def xxxtest__and__(self):
    result = self.cmda and self.cmdb
    self.assert_(isinstance(result, CommandCallChain))
  
  def test_option(self):
    opt1 = Option('--opt1')
    result = self.cmda -opt1
    self.assert_(opt1 in self.cmda.options)
  
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
    
def test_suite():
  suite = unittest.TestSuite((unittest.makeSuite(CommandTestCase),
          DocTestSuite('pyshin.tests.test_command'),  
         ))
  return suite

if __name__ == '__main__':
  unittest.main()
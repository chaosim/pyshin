import unittest

from zope.testing.doctestunit import DocTestSuite, DocFileSuite
from zope.testing import doctest

import exceptions

from pyshin.command import Command
from pyshin.option import Option#, OptionInstance
#from pyshin.base import fromFunction
from pyshin.call import CommandCall

class CmdA(Command):
  a = Option('-a')
  value = 1
  def action(self):return 'CmdA.action'
cmdA = CmdA()

class CommandTestCase(unittest.TestCase):

  def setUp(self):
    pass
      
  def xxxtest_CommandClassDefine(self):
    ''' class X(Command) should produce an instance of CommandClass'''
    #self.assertEqual(CmdA.__name__, 'CmdA')
    #self.assertEqual(CmdA.__class__, CommandClass)

  def test_OptionInCommand(self):
    '''options should be in options of  the command'''
    self.assert_('a' in  cmdA.options)
    self.assert_(cmdA.options['a']==Option('-a'))  
  
  def test__Command__call__(self):
    '''CommandClass.__call__ produces CommandCall'''
    result = cmdA()
    self.assertEqual(result.__class__, CommandCall)
    self.assertEqual(result.command, cmdA)
    
  def test__InependentCommandCall(self):
    '''CommandCall should not pollute the instance of the command'''
    cmdcall = cmdA()
    cmdcall.value = 2
    self.assertNotEqual(cmdcall.value, cmdA.value)
    
  def test_CommandMethod(self):
    '''"Method" in Command is just a function and becomes the method of the 
    instance of CommandCall'''
    def f():pass
    self.assertEqual(type(cmdA.cmdcallMethods['action']), type(f))
    result = cmdA()
    self.assertEqual(result.action(), 'CmdA.action')
   
def test_suite():
  suite = unittest.TestSuite((unittest.makeSuite(CommandTestCase),
         ))
  return suite

if __name__ == '__main__':
  unittest.main()
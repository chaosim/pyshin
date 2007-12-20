import unittest

from zope.testing.doctestunit import DocTestSuite, DocFileSuite
from zope.testing import doctest

import exceptions

from pyshin.command import Command
from pyshin.option import Option, OptionInstance

class CmdA(Command):
  a = Option('-a')
  def execute(self):return 'CmdA.execute'

class CommandTestCase(unittest.TestCase):

  def setUp(self):
    self.cmda = Command('a', None)
      
  def test_CommandClassDefine(self):
    ''' class X(Command) should produce an instance of CommandClass'''
    self.assertEqual(CmdA.__name__, 'CmdA')
    self.assertEqual(CmdA.__class__, CommandClass)
    self.assertEqual(CmdA.__class__.__name__, 'CommandClass')

  def test_OptionInCommand(self):
    '''options should be defined in the Command '''
    self.assert_('a' in CmdA.options)
    self.assert_(CmdA.options['a']==Option('-a'))
  
  def test_Command__call__(self):
    '''Command.__call__ should produce CommandCall'''
    result = CmdA()
    self.assertEqual(result.__class__, CommandCall)
    self.assertEqual(result.command, CmdA)
    self.assertEqual(result.execute(), 'CmdA.execute')
    
  def xxxtest_addOptionToCall(self):
    ''' cmda/a 
    this should be put in test_cmdcall.py'''
    a = OptionInstance('-a')
    cmd = CmdA()
    result = cmd -a
    self.assertEqual(result.a, True)  
    
def test_suite():
  suite = unittest.TestSuite((unittest.makeSuite(CommandTestCase),
         ))
  return suite

if __name__ == '__main__':
  unittest.main()
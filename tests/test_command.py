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
    pass
      
  def test_CommandClassDefine(self):
    ''' class X(Command) should produce an instance of CommandClass'''
    self.assertEqual(CmdA.__name__, 'CmdA')

  def test_OptionInCommand(self):
    '''options should be defined in the Command '''
    cmda = CmdA()
    self.assert_('a' in cmda.options)
    self.assert_(cmda.options['a']==Option('-a'))  
    self.assertEqual(cmda.execute(), 'CmdA.execute')
    
  def test_addOptionToCommand(self):
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
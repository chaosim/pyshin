import unittest

from pyshin.command import command, CommandClass
from pyshin.option import Option
from pyshin.call import CommandCall
from pyshin.command import importer

class HelpTestCase(unittest.TestCase):
  def setUp(self):
    self.importer = importer(globals())
    
  def test_help(self):
    from pyshin.tests.commands import HelpCommand as cmd1
    cmdcall = cmd1 -h
    cmdcall.execute()
    self.assertEqual(cmdcall.result, 'base command with help support')

  def test_help2(self):
    from pyshin.tests.commands import HelpCommand as cmd1
    cmdcall = cmd1 -x
    cmdcall.execute()
    self.assertEqual(cmdcall.result, 'execute with -x')
    
  def tearDown(self):
    del self.importer

def test_suite():
  suite = unittest.TestSuite((
            unittest.makeSuite(HelpTestCase),
          ))
  return suite

if __name__ == '__main__':
  unittest.main()
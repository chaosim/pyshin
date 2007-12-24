import unittest

from zope.testing.doctestunit import DocTestSuite, DocFileSuite
from zope.testing import doctest

def test_suite():
    suite = unittest.TestSuite((
                DocFileSuite('..\\readme.txt',
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
           ))
    return suite

if __name__ == '__main__':
    unittest.main()
pyshin

What's pyshin?
    Pyshin is NOT python, it's NOT a misspelling of python either. 
    PYSHON is a PY-thon SH-ell IN python shell. 
    Pyshin is a shell of the python, by the python, and for the python. 
    So What is it really? 
    * It's a shell. So you can use it like csh, bash on Unix, or DOS shell, PowerShell on Windows.
    * It uses the syntax of the python to simulate the shell syntax.
    * It is a package writen by the python.
    * It is used for the python. You can import import in any python shell and excute all of the commands. You can import pyshin from your package or application of python and use the commands in your program.
    We pythoners love PYSHIN!

Get Started
  First, just import something from pyshin.    
    >>> from pyshin import *
    
  And then, some commands used most frequently.
  
    >>> cd(r'e:\zope3\lib\python\pyshin')
    e:\zope3\lib\python\pyshin
    >>> cd
    e:\zope3\lib\python\pyshin
    >>> cwd
    e:\zope3\lib\python\pyshin

    XXX >>> from pyshin.shell import Shell
    XXX >>> from pyshin.command import Command
    XXX >>> import os
    XXX >>> sh = Shell([Command('cwd',os.getcwd)])
    XXX >>> print sh
    python shell

    XXX >>> cwd = Command('',os.getcwd)
    XXX >>> cwd
    e:\zope3\lib\python\pyshin

    >>> dir(r'e:\zope3\lib\python\pyshin\tests\testdir')
    ['1.txt', '2.txt']
    >>> cd(r'e:\zope3\lib\python\pyshin\tests\testdir')
    e:\zope3\lib\python\pyshin\tests\testdir
    >>> dir
    ['1.txt', '2.txt']

Advance Uses


Extend pyshin
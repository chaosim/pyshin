'''buitlin commands frequently used '''

'''builtin commands should not have common code, such as > < | repr str 
__getattr__'''

from command import Command
from pyshin.option import Option, OptionContainer

import os
import dircache

class _Cwd(Command):
  '''should base on Command class which don't need any option and arguments'''
  nargs = 0
  def execute(self):
    ''''''
    #return os.getcwd()
    
cwd = _Cwd()

class _Cd(Command):
  '''should base on Command class which allow dotted path as arguments'''
  dir = path = Option('--path', '-p', action='store')
  
  def execute(self):
    os.chdir(self.dir)
    return os.getcwd()
  
cd = _Cd()

class _Dir(Command):
  '''should base on Command class which allow dotted path as arguments'''
  
  def __init__(self):
    self.path = ''
  def __call__(self, path):
    if self.path!='': 
      # dir.path.to.here(path)
      # 应该提示用法
      # 如果是非交互使用应该提示语法错误
      pass
    print dircache.listdir(path)
  def __getattr__(self,attr):
    ''' dir.path.to.here'''
    # dir(jgksdfjkl).dfasf.dsfas.dasfsda: syntax error
    self.path += attr
    
    
  def __repr__(self):
    return repr(dircache.listdir(os.getcwd()))

dir = _Dir()

class _Notepad(Command):
  '''should base on Command class which allow dotted path as arguments'''
  def execute(self):
    if file is None:
      os.spawnl(os.P_NOWAIT, r'c:\windows\notepad.exe')
    else: os.system(r'c:\windows\notepad.exe %s'%file)
##sh.addCommand(command('notepad',notepad))
##sh.notepad(r'e:\cxm\temp.r')

#sh.cd('c:\\') 



def shopen(path):
  os.startfile(path)  
##sh.addCommand(command('shopen',shopen))
#sh.shopen(r'e:\cxm\temp.r')

class _Open(Command):
  """should base on Command class which allow dotted path filename as arguments"""
  def __init__(self):
    super(_Open, self).__init__(None, None)
    self.path = ''
  def __getattr__(self, attr):
    try:
      return super(_Open, self).__getattr__(attr)
    except:
      if self.path=='':
        self.path += attr
      else:
        self.path += '.'+attr
      return self

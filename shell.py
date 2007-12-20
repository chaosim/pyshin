import os
class xxxshell:
  def __init__(self,cmd=None):
    self.cmd = {}
    if cmd is not None and type(cmd)==type([]):
      for c in cmd:
        self.addCommand(c)
    else: raise 'shell must be given a command list.'
  
  def __getattr__(self, attr):
    try: return self.cmd[attr]()
    except: 
      try: return self.cmd[attr] 
      except: pass
      
  def addCommand(self, cmd):
    self.cmd[cmd.name] = cmd
  def commands(self):
    for x in self.cmd:
      print x  
  def __str__(self):
    return 'python shell'

class Shell:
  '''command shell'''
  def __init__(self, cmd):
    self.cmd = {}
    if cmd is not None:
      for c in cmd:
        # print c
        self.addCommand(c)
  def __getattr__(self, attr):
    try: return self.cmd[attr]
    except:pass    
  def __str__(self):
    return 'python shell'
      
  def addCommand(self, cmd):
    self.cmd[cmd.name] = cmd
        
class History:
  '''history of a session in shell''' 
  def __init__(self):
    self.calls = None
             
    
sh = shell([command('cwd', os.getcwd)])
print sh
print sh.cwd

##for x in os.__dict__:
##  if type(os.__dict__[x])==type(os.chmod):
##    print x
#stop
    
#print sh.commands()
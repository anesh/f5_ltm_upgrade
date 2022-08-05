import os

def check(hostname):
  flag = True
  response = os.system("ping -c 1 " + hostname +" > /dev/null 2>&1")
  while(flag):
    response = os.system("ping -c 1 " + hostname +" > /dev/null 2>&1")
    if response == 0:
      state = 'up'
      print "F5 is UP"
      flag = False
    else:
      print "F5 is rebooting"
      state = 'down'
  return state

check('10.124.5.243')

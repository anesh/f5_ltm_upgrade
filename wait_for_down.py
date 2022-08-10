import os

def check(hostname):
  flag = True
  while(flag):
    response = os.system("ping -c 10 " + hostname +" > /dev/null 2>&1")
    if response == 0:
      print "F5 is UP, going to reboot"
    else:
      flag = False
      state = "rebooted"
  return state


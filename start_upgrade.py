import os
import datetime
import requests
import json
import backup
import load_config
import failover_status
requests.packages.urllib3.disable_warnings()

f1 = open('/home/anesh/f5devices.txt', 'r')

devices = f1.readlines()
username = os.environ['f5username']
password = os.environ['f5password']

for device in devices:
  temp_date = str(datetime.datetime.utcnow())
  split_date = str.split(temp_date)
  my_date = split_date[0]

  column = device.split()
  filename = column[0]+ my_date
  try:
    standbydevice = failover_status.get()
    '''
    print "saving current running configuration"
    load_config.save(column[1],username,password)
    print "verifying running configuration for errors"
    load_config.load_verify(column[1],username,password)
    print "saving ucs and qkview files"    
    backup.start_backup(column[1],username,password,filename)
    '''
    if standbydevice['device'] ==  column[1]
       
  except Exception as e:
    print e


f1.close()


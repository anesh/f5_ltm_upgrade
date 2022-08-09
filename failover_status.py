import os
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()
import traceback

f1 = open('/home/ctc/f5devices.txt', 'r')
devices = f1.readlines()
username = os.environ['f5username']
password = os.environ['f5password']


def get():
  device_fo = {}
  print "Checking failover status"
  try:
    for device in devices:
      column = device.split()
      r = requests.get("https://"+column[1]+"/mgmt/tm/cm/failover-status",auth=(username,password),verify=False)
      status =  r.json()
      nestedstat = status['entries']['https://localhost/mgmt/tm/cm/failover-status/0']['nestedStats']['entries']
      state = nestedstat['status']['description']
      if state == "ACTIVE":
        device_fo['active'] = column[1]
      if state == "STANDBY":
        device_fo['standby']= column[1]
    #get traffic group
    #nestedstat_details =  nestedstat['https://localhost/mgmt/tm/cm/failoverStatus/0/details']['nestedStats']['entries']
    #traffic_group = nestedstat_details['https://localhost/mgmt/tm/cm/failoverStatus/0/details/0']['nestedStats']['entries']['details']['description']
    #print traffic_group.strip('active for ')
  except Exception as e:
    print e
    print(traceback.format_exc())

  return device_fo






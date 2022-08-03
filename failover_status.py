import os
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()

f1 = open('/home/anesh/f5devices.txt', 'r')
devices = f1.readlines()
username = os.environ['f5username']
password = os.environ['f5password']


def get():
  standbydevice = {}
  print "Checking failover status"
  try:
    for device in devices:
      column = device.split()
      r = requests.get("https://"+column[1]+"/mgmt/tm/cm/failover-status",auth=(username,password),verify=False)
      status =  r.json()
      nestedstat = status['entries']['https://localhost/mgmt/tm/cm/failover-status/0']['nestedStats']['entries']
      state = nestedstat['status']['description']
      if state == "ACTIVE":
        print "performing config sync from ACTIVE TO STANDBY"
        headers = {'Content-type':'application/json'}
        sync_payload = {"command":"run","utilCmdArgs":"config-sync to-group Failover_Sync"}
        r = requests.post("https://"+column[1]+"/mgmt/tm/cm",data=json.dumps(sync_payload),auth=(username,password),headers=headers,verify=False)
        print r.status_code
        load_data =  r.json()
        print load_data

      if state == "STANDBY":
        standbydevice['device']= column[1]
    #get traffic group
    #nestedstat_details =  nestedstat['https://localhost/mgmt/tm/cm/failoverStatus/0/details']['nestedStats']['entries']
    #traffic_group = nestedstat_details['https://localhost/mgmt/tm/cm/failoverStatus/0/details/0']['nestedStats']['entries']['details']['description']
    #print traffic_group.strip('active for ')
  except Exception as e:
    print e

  return standbydevice




import os
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()



def start(username,password,device):
  try:
    print "performing config sync from ACTIVE TO STANDBY" 
    headers = {'Content-type':'application/json'}
    sync_payload = {"command":"run","utilCmdArgs":"config-sync to-group Failover_Sync"}
    r = requests.post("https://"+device+"/mgmt/tm/cm",data=json.dumps(sync_payload),auth=(username,password),headers=headers,verify=False)
    print r.status_code
    load_data =  r.json()
    print load_data

  except Exception as e:
    print e





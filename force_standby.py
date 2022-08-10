import os
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()



def post(username,password,device):
  try:
    headers = {'Content-type':'application/json'}
    standby_payload = {"command":"run","utilCmdArgs":"-c 'tmsh run sys failover standby'"}
    r = requests.post("https://"+device+"/mgmt/tm/util/bash",data=json.dumps(standby_payload),auth=(username,password),headers=headers,verify=False)
    print r.status_code
    load_data =  r.json()
    print load_data

  except Exception as e:
    print e





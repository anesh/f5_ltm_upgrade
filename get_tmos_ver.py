import os
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()



def start(username,password,device):
  try:
    headers = {'Content-type':'application/json'}
    r = requests.get("https://"+device+"/mgmt/tm/sys/version",auth=(username,password),headers=headers,verify=False)
    load_data =  r.json()
    selflink = load_data['entries']['https://localhost/mgmt/tm/sys/version/0']['nestedStats']['entries']
    version = selflink['Version']['description']
    build = selflink['Build']['description']
    print version
    print build

  except Exception as e:
    print e
  return version





import os
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()



def start(username,password,device):
  flag = True
  while(flag):
    try:
      headers = {'Content-type':'application/json'}
      r = requests.get("https://"+device+"/mgmt/tm/sys/service/mcpd/stats",auth=(username,password),headers=headers,verify=False)
      load_data =  r.json()
      state = load_data['apiRawValues']['apiAnonymous']
      if "run" in state:
        flag = False
        print "mcpd is up"
        state = "mcpdup"
    except:
      print "mcpd is down"
  return state






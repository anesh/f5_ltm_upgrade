import os
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()

def load_verify(hostname,username,password):
  print "verify config load for errors"
  try:
    headers = {'Content-type':'application/json'}
    load_payload = {"command":"run","utilCmdArgs":"-c 'tmsh load sys config partitions all verify'"}
    r = requests.post("https://"+hostname+"/mgmt/tm/util/bash",data=json.dumps(load_payload),auth=(username,password),headers=headers,verify=False)
    load_data =  r.json()
    print load_data['commandResult']    
    if "Error" in load_data['commandResult']:
      sys.exit("""
               FOUND ERRORS in configuration file.. 
               Rectify errors and run below commands and then re-run script..
               tmsh save sys config partitions all
               tmsh load sys config partitions all""")
    else:
      print "VALIDATION OF CONFIG SUCCESSFUL"
  except Exception as e:
    print e

def save(hostname,username,password):
  print "Saving config on all partitions"
  try:
    headers = {'Content-type':'application/json'}
    save_payload = {"command":"save"}
    r = requests.post("https://"+hostname+"/mgmt/tm/sys/config",data=json.dumps(save_payload),auth=(username,password),headers=headers,verify=False)
    load_data =  r.json()
    print load_data
  except Exception as e:
    print e




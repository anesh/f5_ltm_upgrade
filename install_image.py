import os
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()

def get_volumes(hostname,username,password):
  try:
    headers = {'Content-type':'application/json'}
    r = requests.get("https://"+hostname+"/mgmt/tm/sys/software/volume",auth=(username,password),headers=headers,verify=False)
    load_data =  r.json()
    for data in load_data['items']:
      print data['status']
      print data['name']
      print data['active']
  except Exception as e:
    print e

def install(hostname,username,password,image_name):
  try:
    headers = {'Content-type':'application/json'}
    load_payload = {"command":"install","name":image_name,"volume":vname}
    r = requests.post("https://"+hostname+"/mgmt/tm/sys/software/image",data=json.dumps(load_payload),auth=(username,password),headers=headers,verify=False)
    print r.status_code
    r = requests.get("https://"+hostname+"/mgmt/tm/sys/software/volume/"+vname,auth=(username,password),headers=headers,verify=False)
    data = r.json()
    status = data[0]['items']['status']
    while(status!="complete"):
      r = requests.get("https://"+hostname+"/mgmt/tm/sys/software/volume/"+vname,auth=(username,password),headers=headers,verify=False)
      data = r.json()
      status = data[0]['items']['status']
    print "Installation complete"
  except Exception as e:
    print e

def change_boot(hostname,username,password)
  try:
    headers = {'Content-type':'application/json'}
    load_payload = {"command":"reboot","volume":vname}
    r = requests.post("https://"+hostname+"/mgmt/tm/sys",data=json.dumps(load_payload),auth=(username,password),headers=headers,verify=False)
    print r.status_code
  except Exception as e:
    print e


get_volumes("192.168.2.66","admin","p@ssword123")


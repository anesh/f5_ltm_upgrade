import os
import requests
import json
import sys
import time
requests.packages.urllib3.disable_warnings()

def get_volumes(hostname,username,password):
  try:
    headers = {'Content-type':'application/json'}
    r = requests.get("https://"+hostname+"/mgmt/tm/sys/software/volume",auth=(username,password),headers=headers,verify=False)
    load_data =  r.json()
    for data in load_data['items']:
      if data.get('active'):
        print data['name']+" is the active partition"
      else:
        vname = data['name']
        print vname +" is Free"
      
  except Exception as e:
    print e
  return vname

def install(hostname,username,password,image_name,vname):
  try:
    volume = vname.split('.')
    getvolnum = volume[1]
    headers = {'Content-type':'application/json'}
    load_payload = {"command":"install","name":image_name,"volume":vname}
    r = requests.post("https://"+hostname+"/mgmt/tm/sys/software/block-device-image",data=json.dumps(load_payload),auth=(username,password),headers=headers,verify=False)
    print r.status_code
    print r.text
    time.sleep(5)
    flag = True
    while(flag):
      r = requests.get("https://"+hostname+"/mgmt/tm/sys/software/volume/",auth=(username,password),headers=headers,verify=False)
      data = r.json()
      if getvolnum == '1':
         status = data['items'][0]['status']
         print status
      if getvolnum == '2':
        status = data['items'][1]['status']
        print status
      if getvolnum == '3':
        status = data['items'][2]['status']
        print status
      if status == 'complete':
        flag = False
    print "Installation complete"
  except Exception as e:
    print e
  return status 

def change_boot(hostname,username,password,vname):
  try:
    headers = {'Content-type':'application/json'}
    load_payload = {"command":"reboot","volume":vname}
    r = requests.post("https://"+hostname+"/mgmt/tm/sys",data=json.dumps(load_payload),auth=(username,password),headers=headers,verify=False)
    print r.status_code
  except Exception as e:
    print e


#get_volumes("10.124.5.243","admin","born2run")
#install("10.124.5.243","admin","born2run","BIGIP-15.1.4.1-0.0.15.iso","HD1.2")
#change_boot("10.124.5.243","admin","born2run","HD1.3")

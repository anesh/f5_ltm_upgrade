import os
import requests
import json
import sys
import time
import sys
from helper import retry
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

@retry(times=2, exceptions=(ValueError))
def install(hostname,username,password,image_name,vname,resturi):
  volume = vname.split('.')
  getvolnum = volume[1]
  headers = {'Content-type':'application/json'}
  load_payload = {"command":"install","name":image_name,"volume":vname}
  r = requests.post("https://"+hostname+"/"+resturi,data=json.dumps(load_payload),auth=(username,password),headers=headers,verify=False)
  http_code = r.status_code
  if "400" in str(http_code):
    sys.exit("IMAGE INSTALLATION FAILED MANUAL INTERVENTION REQUIRED!!!")
  print r.text
  time.sleep(5)
  flag = True
  while(flag):
    r = requests.get("https://"+hostname+"/mgmt/tm/sys/software/volume/",auth=(username,password),headers=headers,verify=False)
    http_code = r.status_code
    if "400" in str(http_code):
      sys.exit("IMAGE INSTALLATION FAILED MANUAL INTERVENTION REQUIRED!!!")
    data = r.json()
    if getvolnum == '1':
      status = data['items'][0]['status']
      print status
      if 'media' in status:
        counter += 1
        raise ValueError('The requested product/version/build is not in the media')
    if getvolnum == '2':
      status = data['items'][1]['status']
      print status
      if 'media' in status:
        counter += 1
        raise ValueError('The requested product/version/build is not in the media')

    if getvolnum == '3':
      status = data['items'][2]['status']
      print status
      if 'media' in status:
        counter += 1
        raise ValueError('The requested product/version/build is not in the media')

    if status == 'complete':
      flag = False
  print "Installation complete"
  return status 

def change_boot(hostname,username,password,vname):
  try:
    headers = {'Content-type':'application/json'}
    load_payload = {"command":"reboot","volume":vname}
    r = requests.post("https://"+hostname+"/mgmt/tm/sys",data=json.dumps(load_payload),auth=(username,password),headers=headers,verify=False)
    print r.status_code
  except Exception as e:
    print e



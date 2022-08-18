import os
import requests
import json
import sys
import time
import sys
requests.packages.urllib3.disable_warnings()

f1 = open('/home/ctc/f5devices.txt', 'r')
devices = f1.readlines()
username = os.environ['f5username']
password = os.environ['f5password']


def get():
  for device in devices:
    column = device.split()
    f2 = open(column[1]+'backout.txt', 'w')
    column = device.split()
    headers = {'Content-type':'application/json'}
    r = requests.get("https://"+column[1]+"/mgmt/tm/sys/software/volume",auth=(username,password),headers=headers,verify=False)
    load_data =  r.json()
    for data in load_data['items']:
      if data.get('active'):
        vname =  data['name']
        first_strip = vname.strip('1')
        second_strip = first_strip.strip('/')

        f2.write(column[1]+" "+second_strip)




def change_boot(hostname,username,password,vname):
  try:
    headers = {'Content-type':'application/json'}
    load_payload = {"command":"reboot","volume":vname}
    r = requests.post("https://"+hostname+"/mgmt/tm/sys",data=json.dumps(load_payload),auth=(username,password),headers=headers,verify=False)
    print r.status_code
  except Exception as e:
    print e


get()



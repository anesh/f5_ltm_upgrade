import os
import requests
import json
import sys
import time
import sys
import argparse
requests.packages.urllib3.disable_warnings()

username = os.environ['f5username']
password = os.environ['f5password']

parser = argparse.ArgumentParser(description='''F5 upgrade backout''',formatter_class=argparse.RawDescriptionHelpFormatter)

required = parser.add_argument_group('required arguments')
required.add_argument('-b', '--backoutfile', action='store', dest='backoutfile', help='backout file',required=True)

args = parser.parse_args()
backoutfilefile = args.backoutfile


f1 = open(backoutfilefile,'r')
devices = f1.readlines()

for device in devices:
  column = device.split()
  headers = {'Content-type':'application/json'}
  load_payload = {"command":"reboot","volume":column[1]}
  r = requests.post("https://"+column[0]+"/mgmt/tm/sys",data=json.dumps(load_payload),auth=(username,password),headers=headers,verify=False)
  print r.text
  print r.status_code

f1.close()




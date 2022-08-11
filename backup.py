import os
import datetime
import requests
import json
import file_download
import upload_to_sftp
import time
requests.packages.urllib3.disable_warnings()


def start_backup(hostname,username,password,filename):
  headers = {'Content-type':'application/json'}
  backup_payload = {"command":"save","name":filename}
  state_payload = {'_taskState':'VALIDATING'}
  taskstatus =True
  r = requests.post("https://"+hostname+"/mgmt/tm/task/sys/ucs",data=json.dumps(backup_payload),auth=(username,password),headers=headers,verify=False)
  print r.text
  task_selflink = r.json()
  get_task_uri = task_selflink['selfLink']
  uri = get_task_uri.strip('https://localhost')
  r = requests.put("https://"+hostname+"/"+uri,data=json.dumps(state_payload),auth=(username,password),headers=headers,verify=False)
  print r.text
  time.sleep(10)
  while(taskstatus):
    r= requests.get("https://"+hostname+"/"+uri,auth=(username,password),verify=False)
    state = r.json()
    print state
    if state['_taskState'] == "COMPLETED":
      taskstatus = False
  print "saving ucs completed"
  print "----------------------------"
  print "Downloading UCS to Automation server"
  file_download.download(hostname,(username,password),filename+'.ucs','ucs')
  print "upload UCS to Sftp server"
  upload_to_sftp.upload(filename+'.ucs')
  print "Deleting UCS from F5"
  r = requests.delete("https://"+hostname+"/mgmt/tm/sys/ucs/"+filename+'.ucs',auth=(username,password),headers=headers,verify=False)
  print r.text
  print "saving QKView on the f5"
  qk_payload = {"name":filename+".qkview"}
  r = requests.post("https://"+hostname+"/mgmt/cm/autodeploy/qkview",data=json.dumps(qk_payload),auth=(username,password),headers=headers,verify=False)
  qkview_data = r.json()
  get_id = qkview_data['id']
  r = requests.get("https://"+hostname+"/mgmt/cm/autodeploy/qkview/"+get_id,auth=(username,password),verify=False)
  qkview_status = r.json()
  while(qkview_status['status']!="SUCCEEDED"):
    r = requests.get("https://"+hostname+"/mgmt/cm/autodeploy/qkview/"+get_id,auth=(username,password),verify=False)
    qkview_status = r.json()
    print qkview_status
  print "Downloading QKview to Automation server"
  file_download.download(hostname,(username,password),filename+'.qkview','qkview')

  print "Deleting QKView from F5"
  r = requests.delete("https://"+hostname+"/mgmt/cm/autodeploy/qkview/"+get_id,auth=(username,password),headers=headers,verify=False)
  print r.text
  print "upload qkview to Sftp server"
  upload_to_sftp.upload(filename+'.qkview')


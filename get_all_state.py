import os
import requests
import json
import sys
import get_tmos_ver
requests.packages.urllib3.disable_warnings()

def vip(hostname,username,password,outfile):
  print "getting all vips"
  listofvips=[]
  headers = {'Content-type':'application/json'}
  r = requests.get("https://"+hostname+"/mgmt/tm/ltm/virtual/",auth=(username,password),verify=False)
  load_data =  r.json()
  for item in load_data['items']:
    listofvips.append(item['name'])
  #print "Total VIPS:"+str(len(listofvips))
  totalvips = "Total VIPS:"+str(len(listofvips))
  outfile.write(str(totalvips + '\n'))
  ver = get_tmos_ver.start(username,password,hostname)
  for vip in listofvips:
    r = requests.get("https://"+hostname+"/mgmt/tm/ltm/virtual/"+vip+"/stats",auth=(username,password),verify=False)
    data =  r.json()
    if "13" in ver:
      vipr= vip+"=>"+data['entries']['https://localhost/mgmt/tm/ltm/virtual/'+vip+'/~Common~'+vip+'/stats']['nestedStats']['entries']['status.availabilityState']['description']
    else:
      vipr= vip+"=>"+data['entries']['https://localhost/mgmt/tm/ltm/virtual/~Common~'+vip+'/stats']['nestedStats']['entries']['status.availabilityState']['description']
    outfile.write(str(vipr + '\n'))

def pool(hostname,username,password,outfile):
  print "getting all pool"
  listofpools=[]
  listofmem =[]
  headers = {'Content-type':'application/json'}
  r = requests.get("https://"+hostname+"/mgmt/tm/ltm/pool/",auth=(username,password),verify=False)
  load_data =  r.json()
  for item in load_data['items']:
    listofpools.append(item['name'])
  #print "Total POOLS:"+str(len(listofpools))
  totalpools = "Total POOLS:"+str(len(listofpools))
  outfile.write(str(totalpools + '\n'))
  ver = get_tmos_ver.start(username,password,hostname)
  for pool in listofpools:
    r = requests.get("https://"+hostname+"/mgmt/tm/ltm/pool/"+pool+"/stats",auth=(username,password),verify=False)
    data =  r.json()
    if "13" in ver:
      poolname = pool+"=>"+data['entries']['https://localhost/mgmt/tm/ltm/pool/'+pool+'/~Common~'+pool+'/stats']['nestedStats']['entries']['status.availabilityState']['description']
    else:
      poolname = pool+"=>"+data['entries']['https://localhost/mgmt/tm/ltm/pool/~Common~'+pool+'/stats']['nestedStats']['entries']['status.availabilityState']['description']
    outfile.write(str(poolname + '\n'))
    mem_response = requests.get("https://"+hostname+"/mgmt/tm/ltm/pool/"+pool+"/members",auth=(username,password),verify=False)
    mem_data = mem_response.json()
    for mem_item in mem_data['items']:
      listofmem.append(mem_item['name'])
      mem = mem_item['name']
      r = requests.get("https://"+hostname+"/mgmt/tm/ltm/pool/"+pool+"/members/"+mem+"/stats",auth=(username,password),verify=False) 
      pool_mem_status = r.json()
      poolmem =  "*"+mem+"=>"+pool_mem_status['entries']['https://localhost/mgmt/tm/ltm/pool/'+pool+'/members/'+mem+'/~Common~'+pool+'/stats']['nestedStats']['entries']['status.availabilityState']['description']
      outfile.write(str(poolmem + '\n'))





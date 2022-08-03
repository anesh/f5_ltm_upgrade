import os
import requests
import json
import sys
requests.packages.urllib3.disable_warnings()

def vip(hostname,username,password):
  print "getting all vips"
  listofvips=[]
  try:
    headers = {'Content-type':'application/json'}
    r = requests.get("https://"+hostname+"/mgmt/tm/ltm/virtual/",auth=(username,password),verify=False)
    load_data =  r.json()
    for item in load_data['items']:
      listofvips.append(item['name'])
    print "Total VIPS:"+str(len(listofvips))
    for vip in listofvips:
      r = requests.get("https://"+hostname+"/mgmt/tm/ltm/virtual/"+vip+"/stats",auth=(username,password),verify=False)
      data =  r.json()
     
      print vip+"=>"+data['entries']['https://localhost/mgmt/tm/ltm/virtual/~Common~'+vip+'/stats']['nestedStats']['entries']['status.availabilityState']['description']
  except Exception as e:
    print e

def pool(hostname,username,password):
  print "getting all pool"
  listofpools=[]
  listofmem =[]
  try:
    headers = {'Content-type':'application/json'}
    r = requests.get("https://"+hostname+"/mgmt/tm/ltm/pool/",auth=(username,password),verify=False)
    load_data =  r.json()
    for item in load_data['items']:
      listofpools.append(item['name'])
    print "Total POOLS:"+str(len(listofpools))
    for pool in listofpools:
      r = requests.get("https://"+hostname+"/mgmt/tm/ltm/pool/"+pool+"/stats",auth=(username,password),verify=False)
      data =  r.json()

      print pool+"=>"+data['entries']['https://localhost/mgmt/tm/ltm/pool/~Common~'+pool+'/stats']['nestedStats']['entries']['status.availabilityState']['description']

      mem_response = requests.get("https://"+hostname+"/mgmt/tm/ltm/pool/"+pool+"/members",auth=(username,password),verify=False)
      mem_data = mem_response.json()
      for mem_item in mem_data['items']:
        listofmem.append(mem_item['name'])
      for mem in listofmem:
        r = requests.get("https://"+hostname+"/mgmt/tm/ltm/pool/"+pool+"/members/"+mem+"/stats",auth=(username,password),verify=False) 
        pool_mem_status = r.json()
        print "*"+mem+"=>"+pool_mem_status['entries']['https://localhost/mgmt/tm/ltm/pool/'+pool+'/members/'+mem+'/~Common~'+pool+'/stats']['nestedStats']['entries']['status.availabilityState']['description']
  except Exception as e:
    print e



vip("192.168.2.66","admin","p@ssword123")
pool("192.168.2.66","admin","p@ssword123")


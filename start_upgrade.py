import os
import datetime
import requests
import json
import backup
import load_config
import failover_status
requests.packages.urllib3.disable_warnings()

f1 = open('/home/anesh/f5devices.txt', 'r')

devices = f1.readlines()
username = os.environ['f5username']
password = os.environ['f5password']

for device in devices:
  temp_date = str(datetime.datetime.utcnow())
  split_date = str.split(temp_date)
  my_date = split_date[0]

  column = device.split()
  filename = column[0]+ my_date
  try:
    
    if  device_fo['active'] == column[1]:
      print "saving current running configuration"
      load_config.save(column[1],username,password)
      print "verifying running configuration for errors"
      load_config.load_verify(column[1],username,password)
      config_sync.start()
    print "saving ucs and qkview files"    
    backup.start_backup(column[1],username,password,filename)
    get_all_state.vip(column[1],username,password)
    get_all_state.pool(column[1],username,password)

    
       
  except Exception as e:
    print e

for device in devices:
  column = device.split()
  device_fo = failover_status.get()  
  if device_fo['standby'] == column[1]:
    vname = install_image.get_volumes(column[1],username,password)
    first_strip = vname.strip('1')
    second_strip = first_strip.strip('/')
    status = install_image.install(column[1],username,password,column[3],second_strip)
    if status == complete:
      install_image.change_boot(column[1],username,password,second_strip)
      time.sleep(5)
      state  = send_ping.check(column[1])
      if state == "down"
        sys.exit("DEVICE HAS NOT COME UP!!!MANUAL INTERVENTION REQUIRED")


for device in devices:
  column = device.split()
  device_fo = failover_status.get()
  current_tmos = get_tmos_ver.start(username,password,column[1])
  if device_fo['active'] == column[1] and current_tmos not in column[3]
    force_standby.post(username,password,column[1])
    if device_fo['standby'] == column[1]:
      vname = install_image.get_volumes(column[1],username,password)
      first_strip = vname.strip('1')
      second_strip = first_strip.strip('/')
      status = install_image.install(column[1],username,password,column[3],second_strip)
      if status == complete:
         install_image.change_boot(column[1],username,password,second_strip)
         time.sleep(5)
         state  = send_ping.check(column[1])
         if state == "down"
           sys.exit("DEVICE HAS NOT COME UP!!!MANUAL INTERVENTION REQUIRED")





    



f1.close()


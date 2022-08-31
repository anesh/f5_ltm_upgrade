## F5 LTM HA pair upgrade Automation

### Description

- the script gathers ucs and qkview from both the device pairs and uploads to an SFTP server defind by environment variables
- it then gathers the state of all the VIPs and Pools from  both device pairs and stores the files locally
- It stores the state of the active volumes from both devices
- it identifies the active device and saves the running config and does a verify load to check for config errors
- it then proceeds to find the standby device and install the image on a inactive volume
- once installation of image is complete it proceeds to reboot to volume with new image
- once the device is up and the mcpd is up, it checks the state of vips/pools with the pre-check, if there are differences
it stops the upgrade, if no differences are identified it proceeds with the next device

### Pre-requisites

* tested with Python2.7
* set below environment variables
  - f5username
  - f5password
  - username_ftp
  - password_ftp
  - server_ip_ftp
* install below python packages
  - pip install paramiko
  - pip install requests
  - pip install json


### Steps to Execute automation:



```
git clone https://github.com/anesh/f5_ltm_upgrade.git
```

```
cd f5_ltm_upgrade
```

* create a file called "f5devices.txt" and add the devices to be upgarded along with image in the below format
```
F5-2-lab 10.124.5.244 BIGIP-15.1.6-0.0.8.iso
F5-1-lab 10.124.5.243 BIGIP-15.1.6-0.0.8.iso
```

* To run the automation exceute the below command
```
python start_upgrade.py

```

### Steps to Backout change the upgrade

```
python backout_upgrade.py -b <deviceip>backout.txt
eg:
python backout_upgrade.py -b 10.124.5.244backout.txt
```

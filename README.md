## F5 LTM HA pair upgrade Automation

### Description

- the script gathers ucs and qkview from both the device pairs and uploads to the the SFTP server
- it then gathers the state of all the VIPs and Pools from  bothe device pairs and stores the files
- It stores the state of the active volumes in bothe devices
- it identifies the active device and saves the running config and does a verify load to check for config errors
- it then proceeds to find the standby device and install the image on a inactive volume
- once installation of image is complete it proceeds to reboot to volume with new image
- once the device is up and the mcpd is up, it checks the state of vips/pools with the pre-check, if there are differences
it stops the upgrade, if no differences are identified it proceeds with the next device

### Pre-requisites

* Make Sure you have the correct bash profile has the below cofigurations

```
alias python=/opt/rh/python27/root/usr/bin/python2.7
source /etc/environment
```


### Steps to Execute automation, once seed file is peer reviewd:


* login to Automation server[10.2.53.22]

```
git clone https://bitbucket.cantire.com/scm/enia/f5.git
```

```
cd f5/implementation/f5_ltm_upgrade
```

* create a file called "f5devices.txt" and add the devices to be upgarded along with image in the below format
```
Gw-cr-F5-2-lab 10.124.5.244 BIGIP-15.1.6-0.0.8.iso
Gw-cr-F5-1-lab 10.124.5.243 BIGIP-15.1.6-0.0.8.iso
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

import paramiko

def upload(filename):
  sftpserver = "192.168.2.50"
  sftpuser = "anesh"
  sftppass = "chakku@chakku1"
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(sftpserver,username=sftpuser,password=sftppass)
  ftp = ssh.open_sftp()
  ftp.put(filename,'/home/anesh/'+filename,confirm=True)
  

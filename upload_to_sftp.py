import paramiko

def upload(filename):
  sftpserver = "10.124.5.234"
  sftpuser = "ctc"
  sftppass = "password"
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(sftpserver,username=sftpuser,password=sftppass)
  ftp = ssh.open_sftp()
  ftp.put(filename,'/home/ctc/'+filename,confirm=True)
  

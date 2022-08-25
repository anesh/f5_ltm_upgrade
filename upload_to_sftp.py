import paramiko

username = os.environ['username_ftp']
password = os.environ['password_ftp']
server_ip = os.environ['server_ip_ftp']

def upload(filename):
  sftpserver = server_ip
  sftpuser = username
  sftppass = password
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(sftpserver,username=sftpuser,password=sftppass)
  ftp = ssh.open_sftp()
  ftp.put(filename,'/'+filename,confirm=True)
  

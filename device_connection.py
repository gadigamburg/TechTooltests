import sys,paramiko

ssh = paramiko.SSHClient()


def establish_connection(ip_host):
    user='root'
    password='sopranos99'
    port=22
    device=ip_host
    client = paramiko.SSHClient()

#    client.load_system_host_keys()
    #client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    client.connect(device,port, user, password)
    sftp = client.open_sftp()
    sftp.put('C:\Users\sergey.meerovich\Desktop\myest\sergey.sh', '/opt/test.sh')

    return client


def run_remote_commands(client,my_command):
    stdin, stdout, stderr = client.exec_command(my_command)
    outlines = stdout.readlines()
    resp = ''.join(outlines)
    print(resp)
   # client.close()

    #sys.exit(0)
def transfer_files(client):
    sftp=client.open_sftp()
    sftp.put('C:/\Users/\sergey.meerovich/\Documents/\notes.txt' '/opt/test.txt')

def close_connection(ssh_client):
    ssh_client.close()

#ssh_client=establish_connection("172.18.8.41")
#status=run_remote_commands(ssh_client,'ls')
#transfer_files(ssh_client)
#if status==0:
#    close_connection(ssh_client)

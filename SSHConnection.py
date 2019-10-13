from paramiko import SSHClient
from ConfigParser import SafeConfigParser
config_parser=SafeConfigParser()
config_parser.read('config.properties')
import paramiko,time
device_ip=config_parser.get('unit_parameters','ip')

class ConnectionToDUT():
    def CreateConnection(self):
        ssh = SSHClient()
        #ssh.load_system_host_keys()
        #ssh.set_missing_host_key_policy(ssh.AutoAddPolicy())
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        server=config_parser.get('unit_parameters','ip')
        user=config_parser.get('unit_parameters','user')
        password=config_parser.get('unit_parameters','password')

        ssh.connect(server,username=user,password=password)
        return ssh
    def RunRemoteCommands(self,user_command):

        client=self.CreateConnection()
        shell = client.invoke_shell()
        _, ssh_stdout, ssh_stderr = client.exec_command(user_command)
        com_out=ssh_stdout.readlines()
        com_out="".join(com_out)
        #print (com_out)
        com_err=ssh_stderr.readlines()
        com_err="".join(com_err)

        return com_out,com_err,shell,client


    def CloseSSHConnection(self,shell,client):
        # Close connection.
        shell.close()
        client.close()

#
# T=SSHConnection()
# out,err,sh,client=T.RunRemoteCommands('ls')
# print out
# time.sleep(10)
# T.CloseSSHConnection(sh,client)
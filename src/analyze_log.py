import os
import paramiko
import sys


if __name__=="__main__":
    hostname = '2.104.13.126'
    password = sys.argv[1]
    username = 'pi'
    port = 22
    
    remotepath = '/var/log/rabbitmq/rabbit@raspberrypi.log'
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password, port=port)

    ftp_client = ssh_client.open_sftp()
    ftp_client.get(remotepath, '../src/log/rabbitmq.log')
    ftp_client.close()


    # Analyze log file







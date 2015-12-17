#!bin/python
import paramiko
import sys
import socket
from multiprocessing.dummy import Pool as ThreadPool 


with open('servers') as server:
    scontent = server.readlines()

with open('passwords') as passw:
    pcontent = passw.readlines()

def checkserver(server):
    for passw in pcontent:
        server = server.rstrip('\n')
        passw = passw.rstrip('\n')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(server, username='root', password=passw, timeout=2)
            ssh.close()
        except socket.gaierror as e:
            return server + " " + str(e)
        except paramiko.ssh_exception.AuthenticationException as e:
            pass
        except NameError as e:
            return server + " " + str(e)
        except socket.error as e:
            return server + " " + str(e)
        else:
            return server + " has password 'root'"
        
        return server + " is ok"
        
pool = ThreadPool(100)

results = pool.map(checkserver, scontent)

pool.close()
pool.join()

for line in results:
    print line

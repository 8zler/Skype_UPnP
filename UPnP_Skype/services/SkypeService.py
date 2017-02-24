from twisted.internet import reactor
from pyupnp.event import EventProperty
from pyupnp.device import Device, DeviceIcon
from pyupnp.logr import Logr
from pyupnp.services import register_action, Service, ServiceActionArgument, ServiceStateVariable
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP
import os,time,threading,alsaaudio,subprocess
from callManager import CallManager
from volumeManager import VolumeManager
from autoanswerclass import SkypeAPI

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')




def read_file(file):
        f = open(file,"r")
        lines = f.readlines()
        res=""
        for line in lines:
                res+=line[:-1]+";"
        res=res[:-1]
        return res

def isIn(allAccount,account):
        print allAccount
        print account
        if account in allAccount:
                return True
        


class SkypeCallingManager(Service):

	version = (1, 0)
	serviceType = "urn:schemas-upnp-org:service:SkypeCallingManager:1"
	serviceId = "urn:upnp-org:serviceId:SkypeCallingManager"

	actions = {
		'addAuthorizedUser': [
			ServiceActionArgument('nickname','in','nickname')
		],
                'getAuthorizedUser': [
			ServiceActionArgument('allUsers_ret','out','allUsers_ret')
		],
                'deleteAuthorizedUser': [
			ServiceActionArgument('nickname','in','nickname')
		],
                'runAutoAcceptAndAnswer': [
			ServiceActionArgument('run','in','run')
		],
                'holdCall': [
			ServiceActionArgument('run','in','run')
		],
                'resumeCall': [
			ServiceActionArgument('run','in','run')
		],
                'addFriend': [
			ServiceActionArgument('nickname','in','nickname')
		],
                'getUsersPendingAuthorisation': [
			ServiceActionArgument('allUsersPendingAuthorisation','out','allUsersPendingAuthorisation')
		],
                'addUsersPendingAuthorisation': [
			ServiceActionArgument('nickname','in','nickname')
		],
                'sendMessage': [
			ServiceActionArgument('nickname','in','nickname'),
                        ServiceActionArgument('content','in','content')
		]
	}
	
	stateVariables = [
		# Variables
		ServiceStateVariable('nickname','string',sendEvents=True),
		ServiceStateVariable('allUsersAuthorized','string',sendEvents=True),
                ServiceStateVariable('allUsers_ret','string',sendEvents=True),
                ServiceStateVariable('run','boolean',sendEvents=True),
                ServiceStateVariable('allUsersPendingAuthorisation','string',sendEvents=True),
                ServiceStateVariable('content','string',sendEvents=True)
                

	]
	
		
	nick=EventProperty('nickname')
	allUsers=EventProperty('allUsersAuthorized',read_file("/home/heitzler/PFE/autorized_person.txt"))
        callMan = CallManager()
        proc = None
        isAutoLunched = False


	@register_action('addAuthorizedUser')
	def add(self,arg):
                print "in addAuthorizedUser"
                self.f = open("/home/heitzler/PFE/autorized_person.txt","a")
                self.f.write(str(arg)+"\n")
                self.f.close()
                print str(arg)+" written in file"

        @register_action('getAuthorizedUser')
	def get(self):
                print "in getAuthorizedUser"
                return {
                        'allUsers_ret':read_file("/home/heitzler/PFE/autorized_person.txt")
                        }

        @register_action('deleteAuthorizedUser')
	def delete(self,arg):
                print "in deleteAuthorizedUser"
                self.data=read_file("/home/heitzler/PFE/autorized_person.txt").split(";")
                if arg in self.data:
                        self.data.remove(arg)
                        self.f=open("/home/heitzler/PFE/autorized_person.txt","w")
                        self.f.write(";".join(self.data))
                        self.f.close()
                        print "user deleted" 
                
        @register_action('holdCall')
	def hold(self,arg):
                print "in holdCall"
                self.callMan.holdcall()
                

        @register_action('resumeCall')
	def resume(self,arg):
                print "in resumeCall"
                self.callMan.resumecall()


        @register_action('addFriend')
	def add(self,arg):
                print "in addFriend"
                self.callMan.addFriend(arg)


        @register_action('getUsersPendingAuthorisation')
	def getPending(self):
                print "in getUsersPendingAuthorisation"
                return {
                        'allUsersPendingAuthorisation':"user1\nuser2\n"#read_file("/home/heitzler/PFE/pending_authorisation.txt")
                        }



        @register_action('addUsersPendingAuthorisation')
	def setPending(self,arg):
                print "in addUsersPendingAuthorisation"
                self.f = open("/home/heitzler/PFE/pending_authorisation.txt","a")
                self.f.write(str(arg)+"\n")
                self.f.close()
                print str(arg)+" written in file"


        @register_action('sendMessage')
	def sendMessage(self,nick,content):
                print "in sendMessage"
                self.callMan.sendMessage(nick,content)
        
                
                


                

        @register_action('runAutoAcceptAndAnswer')
	def run(self,arg):
                print "in runAutoAcceptAndAnswer"
                if bool(int(arg)) and not self.isAutoLunched:
                        self.proc = subprocess.Popen(["python","autoanswer.py"])
                        self.isAutoLunched = True
                elif self.isAutoLunched:
                        self.proc.terminate()
                        self.isAutoLunched = False



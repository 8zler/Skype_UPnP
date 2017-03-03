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

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')




def read_file(file):
        f = open(file,"r")
        lines = f.read()
        lines = lines[:-1]
        res=lines.split(";")
        if res[-1] == '' or res[-1] == ';':
                return ";".join(res)[:-1]
        return ";".join(res)

def delOneUser(fileName,nickname):
        if len(nickname) > 0:
                data = read_file(fileName).split(";")
                print "in del user"
##                print data
##                print "user=|"+nickname+"|"
                if nickname in data:
                        data.remove(nickname)
                        f=open(fileName,"w")
                        for elt in data:
                                f.write(elt+";")
                        f.close()

def addOneUser(fileName,nickname):
        if len(nickname) > 0:                
                f = open(fileName,"a")
                data = read_file(fileName).split(";")
                if nickname not in data:
                        f.write(nickname+";")
                        f.close()
        

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
			ServiceActionArgument('allUsersAuthorized','out','allUsersAuthorized')
		],
                'deleteAuthorizedUser': [
			ServiceActionArgument('nickname','in','nickname')
		],
                'runAutoAcceptAndAnswer': [
			ServiceActionArgument('run','in','run')
		],
                'holdResumeCall': [
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
		],
                'deleteUsersPendingAuthorisation': [
			ServiceActionArgument('nickname','in','nickname')
		],
                'endCall': [
			ServiceActionArgument('run','in','run')
		],
                'getStatus': [
			ServiceActionArgument('status','out','status')
		],
                'setStatus': [
			ServiceActionArgument('status','in','status')
		],
                'setName': [
			ServiceActionArgument('nickname','in','nickname')
		],
                'delFriend': [
			ServiceActionArgument('nickname','in','nickname')
		],
                'getFriend': [
			ServiceActionArgument('friendlist','out','friendlist')
		]
	}
	
	stateVariables = [
		# Variables
		ServiceStateVariable('nickname','string',sendEvents=True),
		ServiceStateVariable('allUsersAuthorized','string',sendEvents=True),
                ServiceStateVariable('run','boolean',sendEvents=True),
                ServiceStateVariable('allUsersPendingAuthorisation','string',sendEvents=True),
                ServiceStateVariable('content','string',sendEvents=True),
                ServiceStateVariable('status','boolean',sendEvents=True),
                ServiceStateVariable('friendlist','string',sendEvents=True)
                

	]
	
		
	nick=EventProperty('nickname')
	stat = EventProperty('status',False)
	allUsersAuthorized=EventProperty('allUsersAuthorized')#,read_file("/home/heitzler/PFE/authorized_person.txt"))
	fdp=EventProperty('allUsersPendingAuthorisation')#read_file("/home/heitzler/PFE/pending_authorisation.txt"))
	FL=EventProperty("friendlist")
        callMan = CallManager()
        proc = None
        isAutoLunched = False


	@register_action('addAuthorizedUser')
	def add(self,arg):
                print "in addAuthorizedUser"
                addOneUser("/home/heitzler/PFE/authorized_person.txt",arg)
                print str(arg)+" written in file"

        @register_action('getAuthorizedUser')
	def authUser(self):
                print "in getAuthorizedUser"
                return {
                        'allUsersAuthorized':read_file("/home/heitzler/PFE/authorized_person.txt")
                        }

        @register_action('deleteAuthorizedUser')
	def delete(self,arg):
                print "in deleteAuthorizedUser "+arg+" deleted"
                delOneUser("/home/heitzler/PFE/authorized_person.txt",arg)
                
        @register_action('holdResumeCall')
	def hold(self,arg):
                print "in holdCall"
                self.callMan.holdResumeCall()


        @register_action('endCall')
	def end(self,arg):
                print "in endCall"
                self.callMan.endCall()


        @register_action('addFriend')
	def addFriend(self,arg):
                print "in addFriend"
                self.callMan.addFriend(arg)


        @register_action('getUsersPendingAuthorisation')
	def getPending(self):
                print "in getUsersPendingAuthorisation"
                return {
                        'allUsersPendingAuthorisation':read_file("/home/heitzler/PFE/pending_authorisation.txt")
                        }

        @register_action('addUsersPendingAuthorisation')
	def setPending(self,arg):
                print "in addUsersPendingAuthorisation"
                addOneUser("/home/heitzler/PFE/pending_authorisation.txt",arg)
                print str(arg)+" written in file"

        @register_action('deleteUsersPendingAuthorisation')
	def delPending(self,arg):
                print "in deleteUsersPendingAuthorisation "+arg+" deleted"
                print "user=|"+arg+"|"
                delOneUser("/home/heitzler/PFE/pending_authorisation.txt",arg)                


        @register_action('sendMessage')
	def sendMessage(self,nick,content):
                print "in sendMessage"
                self.callMan.sendMessage(nick,content)            



        
        @register_action('getStatus')
	def getStatus(self):
                print "in getStatus"
                print self.callMan.getStatus()
                return {
                        'status':self.callMan.getStatus()
                        }


        @register_action('setStatus')
	def setStatus(self,arg):
                self.callMan.setStatus(bool(int(arg)))


        @register_action('setName')
	def setName(self,arg):
                self.callMan.changeDisplayName(arg)


        @register_action('delFriend')
	def delFriend(self,arg):
                print "in delFriend "+arg+" deleted "
                self.callMan.delFriend(arg)


        @register_action('getFriend')
	def getFriend(self):
                print "in getFriend"
                return {
                        'friendlist':self.callMan.getAllFriend()
                        }


                

        @register_action('runAutoAcceptAndAnswer')
	def run(self,arg):
                print "in runAutoAcceptAndAnswer"
                if bool(int(arg)) and not self.isAutoLunched:
                        self.proc = subprocess.Popen(["python","autoanswer.py"])
                        self.isAutoLunched = True
                elif self.isAutoLunched:
                        self.proc.terminate()
                        self.isAutoLunched = False


                        









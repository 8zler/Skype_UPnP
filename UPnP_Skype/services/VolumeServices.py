from twisted.internet import reactor
from pyupnp.event import EventProperty
from pyupnp.device import Device, DeviceIcon
from pyupnp.logr import Logr
from pyupnp.services import register_action, Service, ServiceActionArgument, ServiceStateVariable
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP
import os,time,threading,alsaaudio
from volumeManager import VolumeManager

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')






class VolumeManager(Service):

	version = (1, 0)
	serviceType = "urn:schemas-upnp-org:service:VolumeManager:1"
	serviceId = "urn:upnp-org:serviceId:VolumeManager"

	actions = {
                'setMicVolume': [
			ServiceActionArgument('volume_in','in','volume_in')
		],
                'getMicVolume': [
			ServiceActionArgument('volume_out','out','volume_out')
		]
	}
	
	stateVariables = [
		# Variables
                ServiceStateVariable('volume_in','string',sendEvents=True),
                ServiceStateVariable('volume_out','string',sendEvents=True)
                

	]
	
		
        volMan = VolumeManager()


	

        @register_action('setMicVolume')
	def setvolume(self,arg):                
                self.volMan.setVolume(arg)



        @register_action('getMicVolume')
	def getvolume(self):
                return {
                        'volume_out':self.volMan.getVolume()
                        }

                


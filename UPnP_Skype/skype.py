# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Doc & examples : https://github.com/fuzeman/PyUPnP



from twisted.internet import reactor
from pyupnp.event import EventProperty
from pyupnp.device import Device, DeviceIcon
from pyupnp.logr import Logr
from pyupnp.services import register_action, Service, ServiceActionArgument, ServiceStateVariable
from pyupnp.ssdp import SSDP
from pyupnp.upnp import UPnP
from services import SkypeService,VolumeServices



class RobotDevice(Device):
    deviceType = 'urn:schemas-upnp-org:device:SkypeBot:1'
    friendlyName = "RobotSkype"
    
    def __init__(self):
        Device.__init__(self)
        self.uuid='3a34765e-5e91-4627-b735-1041eaf49740'

        self.skype = SkypeService.SkypeCallingManager()
        self.volum = VolumeServices.VolumeManager()

        
        self.services = [
            self.skype,
            self.volum
        ]

        #self.skype.startRefreshing()

        
        self.icons = [DeviceIcon('image/png', 32, 32, 24,'./skype.png')]

        
if __name__ == '__main__':

    device = RobotDevice()

    upnp = UPnP(device)
    ssdp = SSDP(device)

    upnp.listen()
    ssdp.listen()

    print "Skype services running..."

    reactor.run()
    
        

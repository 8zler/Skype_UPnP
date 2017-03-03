import alsaaudio,os

class VolumeManager:

    def getVolume(self):
        return alsaaudio.Mixer('Capture').getvolume()


    def setVolume(self,value):
        data = int(value.split("Value:")[-1])
        os.system("amixer set 'Capture'"+" "+str(data)+"%")


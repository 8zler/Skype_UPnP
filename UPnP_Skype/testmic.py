import alsaaudio

m = alsaaudio.Mixer('Capture')
print m.volumecap()
m.volumecap()[0].setvolume(20)
print m.getvolume()


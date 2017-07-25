#Script untuk swarming relay (otomatis lho) pada APM:Copter
#dibuat oleh wisnufireball@gmail.com, id Line: wisnufireball
#kalau ada yang mau ditanya, kontak aja.
# Koordinat pake titik
#RUN SCRIPT SETELAH TERBANG

### INISIALISASI ###
print 'Mulai v0.1'
import sys
import clr
import time
clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from MissionPlanner.Utilities import Locationwp

relay_target = Locationwp()	#objek wp, ya bayangkan aja variabel tipe wp
print 'Init Complete'
while True:
	if ((Ports[1].MAV.cs.mode != "Loiter") & (Ports[1].MAV.cs.mode != "Stabilize" )) :
		Locationwp.lat.SetValue(relay_target,(Ports[0].MAV.cs.lat + -6.8868613)/2)
		Locationwp.lng.SetValue(relay_target,(Ports[0].MAV.cs.lng + 107.608548 )/2)
		Locationwp.alt.SetValue(relay_target,10)
		Ports[1].setGuidedModeWP(relay_target)
		print 'Relay Target Updated'
		Script.Sleep(5000)
		
	

print 'Script Selesai'
print 'wisnu emang ganteng'

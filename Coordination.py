#Script untuk swarming relay (otomatis lho) pada APM:Copter
#dibuat oleh wisnu, modif naufalinofh. July 2017
#kalau ada yang mau ditanya, kontak aja.

#RUN SCRIPT SETELAH TERBANG

### INISIALISASI ###
print 'Mulai v0.1'
import sys
import clr
import time
clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from MissionPlanner.Utilities import Locationwp, StreamCombiner
clr.AddReference("MissionPlanner.Controls") # includes the Controls class
from MissionPlanner.Controls import ConnectionControl


class coordinate():
	'show the position in spherical coordinate '
	def __init__(self, lat, lng, alt):
		self.lat = lat
		self.lng = lng
		self.alt = (float) alt

def getPort(int):
	for each var port :
		if (mav.GetParam("SYSID_THISMAV")== 1):
			print "Mission MAV in port"+ mav.GetParam("SYSID_THISMAV")
			return MAV.GetParam 

#Variable. to be fixed
#home = coordinate(someLat, someLon, someAlt)
uavIDRel = 2 #port untuk uav relay
uavIDMis = 3 # port untuk uav misi

home = Locationwp().Set(MAV.getwp(0).lat, MAV.getwp(0).lng, 0, int (MAVLINK.MAV_CMD.WAYPOINT)) #get home coordinate by get value from waypoint 0 / home

relay_target = Locationwp()	#objek wp, ya bayangkan aja variabel tipe wp
print 'Init Complete'
while True:
	while (coordinationStart):
		Locationwp.lat.SetValue(relay_target,(Ports[getPort(uavIDMis)].MAV.cs.lat + home.lat )/2)
		Locationwp.lng.SetValue(relay_target,(Ports[getPort(uavIDRel)].MAV.cs.lng + home.lng )/2)
		Locationwp.alt.SetValue(relay_target,home.alt/2)
		Ports[uavRel].setGuidedModeWP(relay_target)
		print 'Relay Target Updated'
		Script.Sleep(5000)


print 'Script Selesai'
print 'wisnu emang ganteng'+'Fadel lebih ganteng'

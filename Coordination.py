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
from MissionPlanner import MAVLinkInterface
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from MissionPlanner.Utilities import Locationwp, StreamCombiner
#clr.AddReference("MissionPlanner.Controls") # includes the Controls class
#from MissionPlanner.Controls import ConnectionControl


"""
def getPort(int):
	for each var port :
		if (int(Script.GetParam("SYSID_THISMAV"))== 1):
			print "Mission MAV in port"+ Script.GetParam("SYSID_THISMAV")
			return MAV.GetParam 
"""
global relay
global mission
global SLEEPTIME
SLEEPTIME = 5
global VELOCITY
VELOCITY = 23	#for Locust 23, for quad 2

#Variable. as dummy
#home = coordinate(someLat, someLon, someAlt)
relay = 0 #port untuk uav relay
mission = 1 # port untuk uav misi


#FUNCTION
def gps_distance(lat1, lon1, lat2, lon2):
	'''return distance between two points in meters, coordinates are in degrees
	thanks to http://www.movable-type.co.uk/scripts/latlong.html'''
	radius_of_earth = 6378100.0

	from math import radians, cos, sin, sqrt, atan2
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	dLat = lat2 - lat1
	dLon = lon2 - lon1

	a = sin(0.5*dLat)**2 + sin(0.5*dLon)**2 * cos(lat1) * cos(lat2)
	c = 2.0 * atan2(sqrt(a), sqrt(1.0-a))
	return radius_of_earth * c

def safe_distance (portRelay, portMission):
	'''assure that the UAV dont move into each other so close. Prevent clash'''
	dist = gps_distance(Ports[portRelay].MAV.cs.lat,Ports[portRelay].MAV.cs.lng,Ports[portMission].MAV.cs.lat,Ports[portMission].MAV.cs.lng)
	if (dist < (VELOCITY*sleepTime)):
		Script.ChangeMode("Loiter")
	return

def get_homeMission():
	''' get home position from home waypoint in mission UAV'''
	home = Locationwp()  #get home coordinate 
	global mission	#global variable from mission ports
	Locationwp.lat.SetValue(home,MAVLinkInterface.getHomePosition(Ports[mission]).lat)
	Locationwp.lng.SetValue(home,MAVLinkInterface.getHomePosition(Ports[mission]).lng)
	Locationwp.alt.SetValue(home,MAVLinkInterface.getHomePosition(Ports[mission]).alt)
	return home

relay_target = Locationwp()	#objek wp, ya bayangkan aja variabel tipe wp
home = get_homeMission()		# panggil fungsi get_homeMission
print 'Init Complete'
while True:
	#while (coordinationStart):
		Locationwp.lat.SetValue(relay_target,(Ports[uavIDMis].MAV.cs.lat + home.lat )/2)
		Locationwp.lng.SetValue(relay_target,(Ports[uavIDRel].MAV.cs.lng + home.lng )/2)
		Locationwp.alt.SetValue(relay_target,home.alt/2)
		Ports[uavIDRel].setGuidedModeWP(relay_target)
		print 'Relay Target Updated'
		Script.Sleep(sleepTime)



print 'Script Selesai'
print 'wisnu emang ganteng'
print 'Fadel lebih ganteng'

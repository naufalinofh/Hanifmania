#Script untuk coordination relay 
#dibuat oleh wisnufireball@gmail.com, dimodif oleh fadel & hanif. id Line: wisnufireball, hanifmania, naufalinofh
#kalau ada yang mau ditanya, kontak aja.
#Koordinat pake titik
#RUN SCRIPT SETELAH TERBANG

### INITIALIZATION ###

print 'Mulai v1.4'
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

### VARIABLE & CONSTANTS DECLARATION ###

SLEEPTIME = 5
VELOCITY_LOCUST = 23	
VELOCITY_QUAD = 2

SIG_LIMIT
#Variable. as dummy
#home = coordinate(someLat, someLon, someAlt)
uavIDRel = 1 #port untuk uav relay
uavIDMis = 0 # port untuk uav misi

#comment one of these 2 lines below
#VELOCITY = VELOCITY_LOCUST
VELOCITY = VELOCITY_QUAD

### FUNCTION & PROCEDURE DECLARATION ###


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
	global VELOCITY
	global SLEEPTIME
	dist = gps_distance(Ports[portRelay].MAV.cs.lat,Ports[portRelay].MAV.cs.lng,Ports[portMission].MAV.cs.lat,Ports[portMission].MAV.cs.lng)
	if (dist < (VELOCITY*SLEEPTIME)):
		Script.ChangeMode("Loiter")
	return

def safe_signalGCS(portRelay):
	'''failsafe system in case the signal from relay UAV is bad enough'''	
	global SIG_LIMIT
	
def get_homeMission():
	''' get home position from home waypoint in mission UAV'''
	home = Locationwp()  #get home coordinate 
	global mission	#global variable from mission ports
	Locationwp.lat.SetValue(home,MAVLinkInterface.getHomePosition(Ports[mission]).lat)
	Locationwp.lng.SetValue(home,MAVLinkInterface.getHomePosition(Ports[mission]).lng)
	Locationwp.alt.SetValue(home,MAVLinkInterface.getHomePosition(Ports[mission]).alt)
	return home
		
def initialization():
	'''Find and scan the sysid of the all port that connect to the mission planner.'''
	global uavIDRel 	#Sysid for relay UAV
	global uavIDMis		##Sysid for mission UAV
	uavIDRel,uavIDMis = 0,0
	if (Ports[0].MAV.sysid == 1):    # sysid Relay = 1 & sysid Mission = 2
		uavIDRel = 0
		uavIDMis = 1
	else :
		uavIDRel = 1
		uavIDMis = 0
		
def setrelaytarget():
	'''get the location of mission UAV & set new WP for the relay UAV'''
	Locationwp.lat.SetValue(relay_target,(Ports[uavIDMis].MAV.cs.lat + home.lat )/2)
	Locationwp.lng.SetValue(relay_target,(Ports[uavIDMis].MAV.cs.lng + home.lng )/2)
	Locationwp.alt.SetValue(relay_target,8)		Ports[uavIDRel].setGuidedModeWP(relay_target)
	print 'Relay Target Updated'
	
			
### MAIN PROGRAM ###

relay_target = Locationwp()	# objek wp, ya bayangkan aja variabel tipe wp
home = get_homeMission()		# panggil fungsi get_homeMission
print 'Initialization Started...'
initialization()
print 'Initialization Complete'

while True:
	if (Ports[relay].MAV.cs.mode == "Guided") :
		setrelaytarget()
		Script.Sleep(5000)
		
print 'Script Selesai'
print 'wisnu emang ganteng'
print 'Fadel lebih ganteng'
print 'Apalagi Hanif'
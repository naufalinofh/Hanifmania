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
from math import cos, sin, atan2, radians, degrees, sqrt
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

SIG_LIMIT = 40 #percentage of limitation of signal quality from Mission UAV to GCS

uavIDRel = 1 #port untuk uav relay
uavIDMis = 0 # port untuk uav misi

#comment one of these 2 lines below
#VELOCITY = VELOCITY_LOCUST
VELOCITY = VELOCITY_QUAD

### Class Declaration ###
class coordinate:
	'point coordinate on earth'
	def __init__(self, lat, lng, alt):
		self.lat = lat
		self.lng = lng
		self.alt = alt


### FUNCTION & PROCEDURE DECLARATION ###

def gps_distance(p1, p2):
	'''return distance between two points in meters, coordinates are in degrees using Haversine formula
	thanks to http://www.movable-type.co.uk/scripts/latlong.html'''
	radius_of_earth = 6378100.0

	lat1 = radians(p1.lat)
	lat2 = radians(p2.lat)
	lng1 = radians(p1.lng)
	lng2 = radians(p2.lng)
	dLat = lat2 - lat1
	dLng = lng2 - lng1

	a = sin(0.5*dLat)**2 + sin(0.5*dLng)**2 * cos(lat1) * cos(lat2)
	c = 2.0 * atan2(sqrt(a), sqrt(1.0-a))
	return radius_of_earth * c

def safe_distance (portRelay, portMission):
	'''assure that the UAV dont move into each other so close. Prevent clash'''
	global VELOCITY
	global SLEEPTIME
	dist = gps_distance(Ports[portRelay].MAV.cs.lat,Ports[portRelay].MAV.cs.lng,Ports[portMission].MAV.cs.lat,Ports[portMission].MAV.cs.lng)
	if (dist < (VELOCITY*SLEEPTIME)):
		Script.ChangeMode("Loiter")
		Script.Sleep(SLEEPTIME/5)
	return

def safe_signalGCS(portRelay): #EDIT
	'''failsafe system in case the signal from relay UAV is bad enough'''	
	global SIG_LIMIT


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

def get_homeMission():
	''' get home position from home waypoint in mission UAV'''
	home = Locationwp()  #get home coordinate 
	global uavIDMis	#global variable from mission ports
	Locationwp.lat.SetValue(home,MAVLinkInterface.getHomePosition(Ports[uavIDMis]).lat)
	Locationwp.lng.SetValue(home,MAVLinkInterface.getHomePosition(Ports[uavIDMis]).lng)
	Locationwp.alt.SetValue(home,MAVLinkInterface.getHomePosition(Ports[uavIDMis]).alt)
	return home
		
def getBearing(p1, p2):
	'''get degree of line/path relative to north line'''
	'''thanks to http://www.igismap.com/formula-to-find-bearing-or-heading-angle-between-two-points-latitude-longitude/ '''
	dlng = p2.lng-p1.lng
	b = atan2((cos (radians(p2.lat)) * sin(radians(dlng))), ( (cos(radians(p1.lat))*sin(radians(p2.lat))) - ( sin(radians(p1.lat))*cos(radians(p2.lat))*cos(radians(dlng)) )) )
	return b

def setCoordinaterelay(originCoordinate, isBankCW):
	'''set new coordinate to relay based on mission UAV and home coordinate, 
	isBankCW is banking direction of UAV Mission. Value either CW or CCW'''
	R = 6378100 #Radius of the Earth on meters
	d = 40 #Distance in m
	global home
	
	pHome = coordinate(home.lat, home.lng, 0)

	if UAV mission Connect:
		pMis = coordinate (Ports[uavIDMis].MAV.cs.lat, Ports[uavIDMis].MAV.cs.lng, Ports[uavIDMis].MAV.cs.alt)
		bearing = getBearing(pHome, pMis) #bearing of line between home to UAVMission
		if(isBankCW):
			bearing -= radians(90)
		else:
			bearing += radians(90)

		#create straight line from midpoint
		latMid = 0.5 * (pHome.lat + pMis.lat)
		lngMid = 0.5 * (pHome.lng + pMis.lng)

		lat = math.asin( math.sin(latMid)*math.cos(d/R) +
	             math.cos(latMid)*math.sin(d/R)*math.cos(bearing))

		lng = lngMid + math.atan2(math.sin(bearing)*math.sin(d/R)*math.cos(latMid), math.cos(d/R)-math.sin(latMid)*math.sin(lat))
		alt = pMis.alt
		relayCoordinate = coordinate (lat,lng, alt)

		return relayCoordinate

	else:


def setrelaytarget(relay_target,relayCoordinate):
	'''get the location of mission UAV & set new WP for the relay UAV'''
	Locationwp.lat.SetValue(relay_target,relayCoordinate.lat)
	Locationwp.lng.SetValue(relay_target,relayCoordinate.lng)
	Locationwp.alt.SetValue(relay_target,relayCoordinate.alt)		
	Ports[uavIDRel].setGuidedModeWP(relay_target)
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
		Script.Sleep(SLEEPTIME)
		
print 'Script Selesai'
print 'wisnu emang ganteng'
print 'Fadel lebih ganteng'
print 'Apalagi Hanif'



from bluepy.btle import Scanner, DefaultDelegate, Peripheral, Service, Characteristic, UUID
from time import gmtime, strftime
import os
import sys

##############################################
# BluePy Library Notes
##############################################

#1 - Cannot manage to use getCharacteristicsbyUUID() method for UART,
#	 so I hard code the source which is position [0] of characteristic vector

##############################################
# TODO list
##############################################

#TODO: change timeout to 10.0 after tests
#TODO: graphical interface for inputting MAC address and input
#TODO: use just dictionaries when user input the MAC address
#TODO: Check Notifications support on Adafruit board to set delegates and receive
#      notifications assynchronously

##############################################
# Global values for Bluetooth
##############################################

#Using for general storage
SPIRO_MAC_ADDR = 'd0:4f:8f:c9:d0:57'
BNDSW_MAC_ADDR = 'ec:5b:e7:e0:96:c2'
DRILL_MAC_ADDR = 'df:c5:a5:de:ee:9a'
MILLI_MAC_ADDR = 'c6:73:0d:c1:66:ba'
CIRCS_MAC_ADDR = 'ca:58:f6:d6:2f:ae'

#Usign for friendly programming
MAC_DIC = {'BENDSAW':BNDSW_MAC_ADDR, 'DRILL_PRESS':DRILL_MAC_ADDR,
			'MILL':MILLI_MAC_ADDR, 'CIRCULAR_SAW':CIRCS_MAC_ADDR,
			'SPIROMETER':SPIRO_MAC_ADDR}

#UUID for the Bluetooth UART Service based on Nordic Semiconductors Chip
UART_UUID = UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')

#Global dictionary to hold Peripheral objects to nodes
nodes = {}

##############################################
# Global general variables
##############################################
datax = ""
datay = ""
dataz = ""

##############################################
# Override for Scanner Class
##############################################
class ScanDelegate(DefaultDelegate):
    def __inti__(self):
	DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
	if isNewDev:
        print "Discovered device", dev.addr
	elif isNewData:
        print "Received new data from", dev.addr

###############################################
# General Functions
###############################################
def split_accel_data(data):
    global datax, datay, dataz
    list_aux = data.split('X')
    list_aux = list_aux[1].split('Y')
    datax = list_aux[0]
    list_aux = list_aux[1].split('Z')
    datay = list_aux[0]
    dataz = list_aux[1]
    return;

###############################################
# Scanning Devices
###############################################
print " "
print "Scanning devices..."
print " "
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(6.0)

###############################################
# Connecting Devices
###############################################
print " "
print "Connecting to nodes..."
print " "
for dev in devices:
    #Creating Bendsaw Peripheral
	if dev.addr == MAC_DIC['BENDSAW']:
	    print "Device %s (%s) Bendsaw found, connecting..." %(dev.addr, dev.addrType)
	    bndsw = Peripheral(dev.addr, dev.addrType)
		nodes['bendsaw'] = bndsw
	    for (adtype, desc, value) in dev.getScanData():
            print "    %s = %s" % (desc, value)
	    print " "
	
	#Creating Drilling Machine Peripheral
	if dev.addr == MAC_DIC['DRILL_PRESS']:
	    print "Device %s (%s) Bendsaw found, connecting..." %(dev.addr, dev.addrType)
	    drill = Peripheral(dev.addr, dev.addrType)
		nodes['drill_press'] = drill
	    for (adtype, desc, value) in dev.getScanData():
            print "    %s = %s" % (desc, value)
	    print " "
	
	#Creating Circular Saw Peripheral
	if dev.addr == MAC_DIC['CIRCULAR_SAW']:
	    print "Device %s (%s) Bendsaw found, connecting..." %(dev.addr, dev.addrType)
	    circs = Peripheral(dev.addr, dev.addrType)
		nodes['circ_saw'] = circs
	    for (adtype, desc, value) in dev.getScanData():
            print "    %s = %s" % (desc, value)
	    print " "
		
	#Creating Milling Machine Peripheral
	if dev.addr == MAC_DIC['MILL']:
	    print "Device %s (%s) Bendsaw found, connecting..." %(dev.addr, dev.addrType)
	    milli = Peripheral(dev.addr, dev.addrType)
		nodes['milling_machine'] = milli
	    for (adtype, desc, value) in dev.getScanData():
            print "    %s = %s" % (desc, value)
	    print " "
	
	#Creating Spirometer Peripheral
    if dev.addr == MAC_DIC['SPIROMENTER']:
	    print "Device %s (%s) Spirometer found, connecting..." %(dev.addr, dev.addrType)
	    spiro = Peripheral(dev.addr, dev.addrType)
		nodes['spirometer'] = spiro
	    for (adtype, desc, value) in dev.getScanData():
            print "    %s = %s" % (desc, value)
	    print " "
		

#Debugging loop
#while 1:
#    print "BNDSW %s  || SPIRO %s" % (bndsw.getServiceByUUID(UART_UUID).getCharacteristics()[0].read(),
#				     spiro.getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
#end

#Writing to doc loop
#delete old file for testing
os.system("sudo rm data/data_from_nodes.csv")

file = open("data/data_from_nodes.csv", "a")
while 1:
    try:
		#Handling Bendsaw collection of data
		if nodes.has_key('bendsaw') is True:
			data = str(nodes['bendsaw'].getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
			if (data[0]=='X') and ('Y' in data) and ('Z' in data):
				split_accel_data(data)
				file.write("N1, " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", " +datax +", " +datay +", " +dataz)
				
		#Handling Drilling Machine collection of data
		if nodes.has_key('drill_press') is True:
			data = str(nodes['drill_press'].getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
			if (data[0]=='X') and ('Y' in data) and ('Z' in data):
				split_accel_data(data)
				file.write("N2, " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", " +datax +", " +datay +", " +dataz)
				
		#Handling Milling Machine collection of data
		if nodes.has_key('milling_machine') is True:
			data = str(nodes['milling_machine'].getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
			if (data[0]=='X') and ('Y' in data) and ('Z' in data):
				split_accel_data(data)
				file.write("N3, " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", " +datax +", " +datay +", " +dataz)
				
		#Handling Circular Saw collection of data
		if nodes.has_key('circ_saw') is True:
			data = str(nodes['circ_saw'].getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
			if (data[0]=='X') and ('Y' in data) and ('Z' in data):
				split_accel_data(data)
				file.write("N4, " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", " +datax +", " +datay +", " +dataz)
				
		#Handling Spirometer collection of data
		if nodes.has_key('spirometer') is True:
			data = str(nodes['spirometer'].getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
			file.write("N5, " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", " + data)
        
		
		
		#bndsw_data = str(bndsw.getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
        #spiro_data = str(spiro.getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
		

	    #Drop bad packets data from bendsaw sensor
	    #if (bndsw_data[0]=='X') and ('Y' in bndsw_data) and ('Z' in bndsw_data):
        #    split_accel_data(bndsw_data)
        #    file.write("N1, " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", " +datax +", " +datay +", " +dataz)
	    #file.write("N2, " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", " + str(spiro_data))

	    print "."
    except KeyboardInterrupt:
	    print "Python script was killed, closing file..."
	    file.close()
	    sys.exit()

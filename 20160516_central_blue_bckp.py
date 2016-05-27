from bluepy.btle import Scanner, DefaultDelegate, Peripheral, Service, Characteristic, UUID
from time import gmtime, strftime
import os
import sys

#TODO: change timeout to 10.0 after tests
#TODO: graphical interface for inputting MAC address and input

##############################################
# Global values for Bluetooth
##############################################
SPIRO_MAC_ADDR = 'd0:4f:8f:c9:d0:57'
BNDSW_MAC_ADDR = 'ec:5b:e7:e0:96:c2'

UART_UUID = UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')

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
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(6.0)

###############################################
# Connecting Devices
###############################################
print " "
print "Connecting to nodes..."
print " "
for dev in devices:
    if dev.addr == BNDSW_MAC_ADDR:
	print "Device %s (%s) Bendsaw found, connecting..." %(dev.addr, dev.addrType)
	bndsw = Peripheral(dev.addr, dev.addrType)
	for (adtype, desc, value) in dev.getScanData():
	    print "    %s = %s" % (desc, value)
	print " "
    if dev.addr == SPIRO_MAC_ADDR:
	print "Device %s (%s) Spirometer found, connecting..." %(dev.addr, dev.addrType)
	spiro = Peripheral(dev.addr, dev.addrType)
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
    	bndsw_data = str(bndsw.getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
    	spiro_data = str(spiro.getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
	
	#Drop bad packets data from sensor
	if (bndsw_data[0]=='X') and ('Y' in bndsw_data) and ('Z' in bndsw_data):
	    split_accel_data(bndsw_data)
	    file.write("N1, " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", " +datax +", " +datay +", " +dataz)
	file.write("N2, " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", " + str(spiro_data))

	print "."
    except KeyboardInterrupt:
	print "Python script was killed, closing file..."
	file.close()
	sys.exit()
end

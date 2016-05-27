from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(5.0)
ada = []

for dev in devices:
    print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
    #saving the Accel node in position 0
    if dev.addr == 'ec:5b:e7:e0:96:c2':
	ada.append(dev)
    #saving the Spirometer node in position 1
    if dev.addr == 'd0:4f:8f:c9:d0:57':
	ada.append(dev)
    for (adtype, desc, value) in dev.getScanData():
        print "  %s = %s" % (desc, value)

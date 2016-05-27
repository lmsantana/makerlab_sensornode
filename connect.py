from scan import ada
from bluepy.btle import Peripheral, UUID, Service, Characteristic

UART_UUID = UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
TX_UUID = UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')

per1 = Peripheral(ada[0].addr, ada[0].addrType)
per2 = Peripheral(ada[1].addr, ada[1].addrType)


while 1:
    print "N1 %s   ||  N2 %s " % (per1.getServiceByUUID(UART_UUID).getCharacteristics()[0].read(),
					per2.getServiceByUUID(UART_UUID).getCharacteristics()[0].read())
end

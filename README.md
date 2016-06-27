# Makerlab Sensornode
Codes for the Network of sensors collecting data in *maker labs*

They topology used right now consists of a central BLE device (Raspberry Pi 3) connectec and inquiring data from up to 5 BLE peripheral
nodes (Adafruit BLE based on Nordic chip).

Python library is based on BluePy and some of the data acquisitions are hard coded based on the UART Service provided by Nordic.

Next iterations would be:

-Reconnection handling for when devices are droped

-Improve the number of data points we can get per second (up to 9 now divided by the number of devices)

-Test limit of connection with 7 peripherals

-Test battery usage and life time

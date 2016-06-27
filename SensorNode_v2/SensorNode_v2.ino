// Basic demo for accelerometer readings from Adafruit LIS3DH
#include<Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>
#if not defined (_VARIANT_ARDUINO_DUE_X_) && not defined (_VARIANT_ARDUINO_ZERO_)
  #include <SoftwareSerial.h>
#endif

#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_SPI.h"
#include "Adafruit_BluefruitLE_UART.h"
#include "BluefruitConfig.h"

//Bluetooth device data
#define FACTORYRESET_ENABLE         1
#define MINIMUM_FIRMWARE_VERSION    "0.6.6"
#define MODE_LED_BEHAVIOUR          "MODE"

// I2C
Adafruit_LIS3DH lis = Adafruit_LIS3DH();

Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

void setup(void) {

  //For continuos Streaming, I deactivate any Serial communication
  /****************************************************************************
  * Setting Accelerometer configurations
  *****************************************************************************/
  if (!lis.begin(0x18)) {   // change this to 0x19 for alternative i2c address
    return;
  }  
  lis.setRange(LIS3DH_RANGE_4_G);   // 2, 4, 8 or 16 G!
  lis.setDataRate(LIS3DH_DATARATE_100_HZ); //400, 200, 100, 50, 25, 10, 1 Hz
  
  /****************************************************************************
  * Initializing Bluetooth Module
  *****************************************************************************/
  /* Searching the module */
  if (!ble.begin(VERBOSE_MODE) )
  {
    return;
  }
  /* Resetting the module */
  if (FACTORYRESET_ENABLE)
  {
    /* Perform a factory reset to make sure everything is in a known state */
    if ( ! ble.factoryReset() ){
      return;
    }
  }
  /* Disable command echo from Bluefruit */
  ble.echo(false);
  ble.verbose(false);

  /* Wait for connection */
  while (! ble.isConnected()) {
      delay(500);
  }

  /* Change mode LED activity */
  if ( ble.isVersionAtLeast(MINIMUM_FIRMWARE_VERSION) )
  {
    ble.sendCommandCheckOK("AT+HWModeLED=" MODE_LED_BEHAVIOUR);
  }

  /* Change to data mode*/
  ble.setMode(BLUEFRUIT_MODE_DATA);
  
}

void loop() {
  /* Getting raw data 16-bit */
  //lis.read();      // get X Y and Z data at once
  /* Send the raw results */
  //ble.print("X"+String(lis.x) +" Y"+String(lis.y) +" Z"+String(lis.z));
  
  /* Getting normalized values in m/s^2*/ 
  sensors_event_t event; 
  lis.getEvent(&event);

  /* Guard for sending data only when connected */
  if (ble.isConnected()){
    /* Send the results (acceleration is measured in m/s^2) */
    ble.println("X"+String(event.acceleration.x) +"Y"+String(event.acceleration.y) +"Z"+String(event.acceleration.z));
  }

  /* Give a buffer time for the TX FIFO to send and clear */
  delay(1000);
}

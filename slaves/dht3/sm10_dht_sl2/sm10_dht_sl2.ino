// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"

#define LIGHTPIN1 A3
#define LIGHTPIN2 A4
#define LIGHTPIN3 A5

#define DHTPIN1 3
#define DHTPIN2 4
#define DHTPIN3 5

#define DHTTYPE1 DHT22
#define DHTTYPE2 DHT22
#define DHTTYPE3 DHT11

// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.



DHT dht1(DHTPIN1, DHTTYPE1);
DHT dht2(DHTPIN2, DHTTYPE2);
DHT dht3(DHTPIN3, DHTTYPE3);

#include "SimpleModbusSlave.h"

/* 
   SimpleModbusSlaveV10 supports function 3, 6 & 16.
   
   This example code will receive the adc ch0 value from the arduino master. 
   It will then use this value to adjust the brightness of the led on pin 9.
   The value received from the master will be stored in address 1 in its own
   address space namely holdingRegs[].
   
   In addition to this the slaves own adc ch0 value will be stored in 
   address 0 in its own address space holdingRegs[] for the master to
   be read. The master will use this value to alter the brightness of its
   own led connected to pin 9.
   
   The modbus_update() method updates the holdingRegs register array and checks
   communication.

   Note:  
   The Arduino serial ring buffer is 64 bytes or 32 registers.
   Most of the time you will connect the arduino to a master via serial
   using a MAX485 or similar.
 
   In a function 3 request the master will attempt to read from your
   slave and since 5 bytes is already used for ID, FUNCTION, NO OF BYTES
   and two BYTES CRC the master can only request 58 bytes or 29 registers.
 
   In a function 16 request the master will attempt to write to your 
   slave and since a 9 bytes is already used for ID, FUNCTION, ADDRESS, 
   NO OF REGISTERS, NO OF BYTES and two BYTES CRC the master can only write
   54 bytes or 27 registers.
 
   Using a USB to Serial converter the maximum bytes you can send is 
   limited to its internal buffer which differs between manufactures. 
*/

#define  LED 13  

// Using the enum instruction allows for an easy method for adding and 
// removing registers. Doing it this way saves you #defining the size 
// of your slaves register array each time you want to add more registers
// and at a glimpse informs you of your slaves register layout.

//////////////// registers of your slave ///////////////////
enum 
{     
  // just add or remove registers and your good to go...
  // The first register starts at address 0
  DATA0,
       
  DATA1,
  DATA2,
  DATA3,
  DATA4,
  
  DATA5,
  DATA6,
  DATA7,
  DATA8,
  
  DATA9,
  DATA10,
  DATA11,
  DATA12,
   
  HOLDING_REGS_SIZE // leave this one
  // total number of registers for function 3 and 16 share the same register array
  // i.e. the same address space
};

unsigned int holdingRegs[HOLDING_REGS_SIZE]; // function 3 and 16 register array
////////////////////////////////////////////////////////////

void setup()
{
  /* parameters(HardwareSerial* SerialPort,
                long baudrate, 
		unsigned char byteFormat,
                unsigned char ID, 
                unsigned char transmit enable pin, 
                unsigned int holding registers size,
                unsigned int* holding register array)
  */
  
  /* Valid modbus byte formats are:
     SERIAL_8N2: 1 start bit, 8 data bits, 2 stop bits
     SERIAL_8E1: 1 start bit, 8 data bits, 1 Even parity bit, 1 stop bit
     SERIAL_8O1: 1 start bit, 8 data bits, 1 Odd parity bit, 1 stop bit
     
     You can obviously use SERIAL_8N1 but this does not adhere to the
     Modbus specifications. That said, I have tested the SERIAL_8N1 option 
     on various commercial masters and slaves that were suppose to adhere
     to this specification and was always able to communicate... Go figure.
     
     These byte formats are already defined in the Arduino global name space. 
  */
	
  modbus_configure(&Serial, 9600, SERIAL_8N2, 2, 2, HOLDING_REGS_SIZE, holdingRegs);

  // modbus_update_comms(baud, byteFormat, id) is not needed but allows for easy update of the
  // port variables and slave id dynamically in any function.
  
  modbus_update_comms(9600, SERIAL_8N2, 2);
  
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  
  dht1.begin();
  dht2.begin();
  dht3.begin();
}

long i = 0;
void loop()
{
  //digitalWrite(LED, HIGH);
  
  // modbus_update() is the only method used in loop(). It returns the total error
  // count since the slave started. You don't have to use it but it's useful
  // for fault finding by the modbus master.
  
  modbus_update();
  
  holdingRegs[DATA0] = 2;
  //holdingRegs[PWM_VAL] = 2;
  
  //analogRead(A0); // update data to be read by the master to adjust the PWM
  
  //analogWrite(LED, holdingRegs[PWM_VAL]>>2); // constrain adc value from the arduino master to 255
  
  /* Note:
     The use of the enum instruction is not needed. You could set a maximum allowable
     size for holdinRegs[] by defining HOLDING_REGS_SIZE using a constant and then access 
     holdingRegs[] by "Index" addressing. 
     I.e.
     holdingRegs[0] = analogRead(A0);
     analogWrite(LED, holdingRegs[1]/4);
  */
  
  
  
  // Wait a few seconds between measurements.
  //delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
 if(i==0)
 {
  
  digitalWrite(LED, HIGH);

  float t0, h0;
  
  //1
  float t1, h1, hic1, light1;
  t1 = 32768;
  h1 = 32768;
  h0 = dht1.readHumidity();
  t0 = dht1.readTemperature();
  if(!isnan(t0)) {
    t1 = t0;
  }
  if(!isnan(h0)) {
    h1 = h0;
  }
  hic1 = dht1.computeHeatIndex(t1, h1, false);
  light1 = analogRead(LIGHTPIN1);
  //if(light1 > 15) {
  //  light1 = 32768; 
  //}
  
  holdingRegs[DATA1]= light1;
  holdingRegs[DATA2] = (t1 * 100);
  holdingRegs[DATA3] = int(h1 * 100);
  holdingRegs[DATA4] = int(hic1 * 100);

  //2
  float t2, h2, hic2, light2;
  t2 = 32768;
  h2 = 32768;
  h0 = dht2.readHumidity();
  t0 = dht2.readTemperature();
  if(!isnan(t0)) {
    t2 = t0;
  }
  if(!isnan(h0)) {
    h2 = h0;
  }
  hic2 = dht2.computeHeatIndex(t2, h2, false);
  light2 = analogRead(LIGHTPIN2);
  if(light2 > 15) {
    light2 = 32768; 
  }
  
  holdingRegs[DATA5]= light2;
  holdingRegs[DATA6] = (t2 * 100);
  holdingRegs[DATA7] = int(h2 * 100);
  holdingRegs[DATA8] = int(hic2 * 100);

  
  //3
  float t3, h3, hic3, light3;
  t3 = 32768;
  h3 = 32768;
  h0 = dht3.readHumidity();
  t0 = dht3.readTemperature();
  if(!isnan(t0)) {
    t3 = t0;
  }
  if(!isnan(h0)) {
    h3 = h0;
  }
  hic3 = dht3.computeHeatIndex(t3, h3, false);
  light3 = analogRead(LIGHTPIN3);
  if(light3 > 15) {
    light3 = 32768; 
  }
  
  holdingRegs[DATA9]= light3;
  holdingRegs[DATA10] = (t3 * 100);
  holdingRegs[DATA11] = int(h3 * 100);
  holdingRegs[DATA12] = int(hic3 * 100);
  
  digitalWrite(LED, LOW);
}


if(i++ > 1000000) 
{
   i = 0;
}
}

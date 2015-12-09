// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"

#define DHTPIN 9

#define LIGHTPIN A0

// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11
#define DHTTYPE DHT22   // DHT 22  (AM2302)
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
DHT dht(DHTPIN, DHTTYPE);



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
  ADC_VAL,     
  LIGHT,
  TEMP,
  HUM,
  HI, 
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
  dht.begin();
}

long i = 0;
void loop()
{
  //digitalWrite(LED, HIGH);
  // modbus_update() is the only method used in loop(). It returns the total error
  // count since the slave started. You don't have to use it but it's useful
  // for fault finding by the modbus master.
  
  modbus_update();
  
  //holdingRegs[ADC_VAL] = 1;
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
  float t, h, t0, h0;
  t = 32768;
  h = 32768;
  //while(!isnan(t) && !isnan(h)) {
   
   
   h0 = dht.readHumidity();
    // Read temperature as Celsius (the default)
   t0 = dht.readTemperature();
   
   if(!isnan(t0)) {
     t = t0;
   }
   if(!isnan(h0)) {
     h = h0;
   }
  //}// Read temperature as Fahrenheit (isFahrenheit = true)
  //float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  ///if (isnan(h) || isnan(t)) {
    //Serial.println("Failed to read from DHT sensor!");
    //return;
 //   h = 99;
 //   t = 99;
 // }

  // Compute heat index in Fahrenheit (the default)
  //float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  //float t = 10;
  //float h = 20;
  
  float hic = dht.computeHeatIndex(t, h, false);
  
  int light = analogRead(LIGHTPIN);
  if(light > 15) {
   light = 32768; 
  }
  holdingRegs[LIGHT]= analogRead(LIGHTPIN);
  holdingRegs[TEMP] = (t * 100);
  holdingRegs[HUM] = int(h * 100);
  holdingRegs[HI] = int(hic * 100);
digitalWrite(LED, LOW);
}

if(i++ > 1000000) 
{
  i = 0;
}
}

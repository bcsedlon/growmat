#define SLAVEID 2
#define TXPIN 2

// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"
#include <OneWire.h>
#include <DallasTemperature.h>


#define UPDATEINTERVAL  5000

#define  LED 13

/////////////////////////////////
// ANALOG INPUTS
/////////////////////////////////
#define ANAPIN2 A2
#define ANAPIN3 A3

#define ANA_SAMPLES 10

/////////////////////////////////
// DHT
/////////////////////////////////
#define DHTPIN0 3
#define DHTPIN1 4
#define DHTPIN2 5
#define DHTPIN3 6

#define DHTTYPE0 DHT11
#define DHTTYPE1 DHT11
#define DHTTYPE2 DHT11
#define DHTTYPE3 DHT11

#define MAXDHTERRORCOUNT 10

/////////////////////////////////
// EC
/////////////////////////////////
#define EC_SAMPLES 10
#define EC_INPUTPIN 9
#define EC_ENABLEPIN 8

//TODO from modbus
#define ECL_SOLUTION 1.278
#define ECH_SOLUTION 4.523
#define ECL 242
#define ECH 125

/////////////////////////////////
// PH
/////////////////////////////////
#define PH_SAMPLES 10
#define PH_INPUTPIN 0
#define PHTEMP_INPUTPIN 1

//TODO from modbus
#define PH7_SOLUTION 7.00
#define PH4_SOLUTION 4.01
#define PH7 528
#define PH4 655
//#define PH7_SOLUTION 6.86
//#define PH4_SOLUTION 4.00
//#define PH7 628  
//#define PH4 732

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(DHTPIN0);
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);


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


DHT dht0(DHTPIN0, DHTTYPE0);
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

// Using the enum instruction allows for an easy method for adding and 
// removing registers. Doing it this way saves you #defining the size 
// of your slaves register array each time you want to add more registers
// and at a glimpse informs you of your slaves register layout.

//////////////// registers of your slave ///////////////////
enum 
{     
  // just add or remove registers and your good to go...
  // The first register starts at address 0
  DATA0,  //slave id
  DATA1,  //modbus error counter
         
  DATA2,  //temperature 0 1wire 
  DATA3,  //temperature 1 1wire  
  DATA4,  //temperature 2 1wire   
  DATA5,  //temperature 3 1wire 

  DATA6,  //temperature 1  
  DATA7,  //humidity 1  
  DATA8,  //heatindex 1
  DATA9,  //n/a
  
  DATA10,  //temperature 2  
  DATA11,  //humidity 2  
  DATA12,  //heatindex 2
  DATA13,  //light 2

  DATA14,  //temperature 3  
  DATA15,  //humidity 3  
  DATA16,  //heatindex 3
  DATA17,  //light 3

  //EC
  DATA18,  //ec low pulse time  
  DATA19,  //ec hight pulse time
  DATA20,  //ec pulse time
  DATA21,  //ec

  //PH
  DATA22,   //ph analog raw
  DATA23,   //ph
  DATA24,   //ph temp analog raw
  DATA25,   //ph temp
  DATA26,
  DATA27,
  
  HOLDING_REGS_SIZE // leave this one
  // total number of registers for function 3 and 16 share the same register array
  // i.e. the same address space

  /* Note:
     The use of the enum instruction is not needed. You could set a maximum allowable
     size for holdinRegs[] by defining HOLDING_REGS_SIZE using a constant and then access 
     holdingRegs[] by "Index" addressing. 
     I.e.
     holdingRegs[0] = analogRead(A0);
     analogWrite(LED, holdingRegs[1]/4);
  */
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
	
  modbus_configure(&Serial, 9600, SERIAL_8N2, SLAVEID, TXPIN, HOLDING_REGS_SIZE, holdingRegs);

  /* modbus_update_comms(baud, byteFormat, id) is not needed but allows for easy update of the
     port variables and slave id dynamically in any function.
  */
  //modbus_update_comms(9600, SERIAL_8N2, SLAVEID);
  
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  sensors.begin();
  
  //dht0.begin();
  dht1.begin();
  dht2.begin();
  dht3.begin();

  pinMode(ANAPIN2, INPUT);
  pinMode(ANAPIN3, INPUT);

  pinMode(EC_INPUTPIN ,INPUT);
  pinMode(EC_ENABLEPIN ,OUTPUT);

  pinMode(PH_INPUTPIN, INPUT);
  pinMode(PHTEMP_INPUTPIN, INPUT);

}

double analogRead(int pin, int samples){
  int result = 0;
  for(int i=0; i<samples; i++){
    result += analogRead(pin);
  }
  return (double)(result / samples);
}

void readDHT(DHT dht, float *temperature, float *humidity, float *heatIndex, int *temperatureErrorCnt, int *humidityErrorCnt, int maxErrorCnt) {
  float t, h;
  t = dht.readTemperature();
  h = dht.readHumidity();
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)

  if(!isnan(t)) {
    *temperatureErrorCnt = 0;
    *temperature = t;
  }
  else {
    *temperatureErrorCnt++;
    if(*temperatureErrorCnt > maxErrorCnt) {
      *temperature = t;
    }
  }
  if(!isnan(h)) {
    *humidityErrorCnt = 0;
    *humidity = h;
  }
  else {
    *humidityErrorCnt++;
    if(*humidityErrorCnt > maxErrorCnt) {
      *humidity = h;
    }
  }
  *heatIndex = dht.computeHeatIndex(*temperature, *humidity, false);
}

int errorcnt = 0;

//0
float temperature0, humidity0, heatIndex0;
int temperatureErrorCnt0, humidityeErrorCnt0;
//1
float temperature1, humidity1, heatIndex1;
int temperatureErrorCnt1, humidityeErrorCnt1;
//2
float temperature2, humidity2, heatIndex2;
int temperatureErrorCnt2, humidityeErrorCnt2;
//3
float temperature3, humidity3, heatIndex3;
int temperatureErrorCnt3, humidityeErrorCnt3;

unsigned long currentMillis, previousMillis;

void loop()
{
  /* modbus_update_comms(baud, byteFormat, id) is not needed but allows for easy update of the
     port variables and slave id dynamically in any function.
  */
  //modbus_update_comms(9600, SERIAL_8N2, SLAVEID);
  
  // modbus_update() is the only method used in loop(). It returns the total error
  // count since the slave started. You don't have to use it but it's useful
  // for fault finding by the modbus master.
  
  errorcnt = modbus_update();
  
  holdingRegs[DATA0] = 2 * 100;
  holdingRegs[DATA1] = errorcnt * 100;


  currentMillis = millis();

  if (currentMillis - previousMillis >= UPDATEINTERVAL) {
    previousMillis = currentMillis;
    updateSensors();
  }
}

void updateSensors() {
  
  digitalWrite(LED, HIGH);
  
  //readDHT(dht0, &temperature0, &humidity0, &heatIndex0, &temperatureErrorCnt0, &humidityeErrorCnt0, MAXDHTERRORCOUNT);
  readDHT(dht1, &temperature1, &humidity1, &heatIndex1, &temperatureErrorCnt1, &humidityeErrorCnt1, MAXDHTERRORCOUNT);
  readDHT(dht2, &temperature2, &humidity2, &heatIndex2, &temperatureErrorCnt2, &humidityeErrorCnt2, MAXDHTERRORCOUNT);
  readDHT(dht3, &temperature3, &humidity3, &heatIndex3, &temperatureErrorCnt3, &humidityeErrorCnt3, MAXDHTERRORCOUNT); 

  sensors.requestTemperatures(); // Send the command to get temperatures
  //temperature0 = sensors.getTempCByIndex(0);
  //0
  holdingRegs[DATA2] = int(100 * sensors.getTempCByIndex(0));
  holdingRegs[DATA3] = int(100 * sensors.getTempCByIndex(1));
  holdingRegs[DATA4] = int(100 * sensors.getTempCByIndex(2));
  holdingRegs[DATA5] = int(100 * sensors.getTempCByIndex(3));

  //1
  holdingRegs[DATA6] = int(temperature1 * 100);
  holdingRegs[DATA7] = int(humidity1 * 100);
  holdingRegs[DATA8] = int(heatIndex1 * 100);
  holdingRegs[DATA9] = 0;

  //2
  holdingRegs[DATA10] = int(temperature2 * 100);
  holdingRegs[DATA11] = int(humidity2 * 100);
  holdingRegs[DATA12] = int(heatIndex2 * 100);
  holdingRegs[DATA13] = analogRead(ANAPIN2, ANA_SAMPLES);

  //3
  holdingRegs[DATA14] = int(temperature3 * 100);
  holdingRegs[DATA15] = int(humidity3 * 100);
  holdingRegs[DATA16] = int(heatIndex3 * 100);
  holdingRegs[DATA17] = analogRead(ANAPIN3, ANA_SAMPLES);

  /////////////////////////////////
  // EC
  /////////////////////////////////
  long lowPulseTime = 0;
  long highPulseTime = 0;
  long pulseTime;
  
  digitalWrite(EC_ENABLEPIN, HIGH); // power up the sensor
  delay(100);
  for(unsigned int j = 0; j < EC_SAMPLES; j++){
        highPulseTime += pulseIn(EC_INPUTPIN, HIGH);
        //if (j == 0 and highPulseTime == 0)
        //    return MINVALUE;
        lowPulseTime += pulseIn(EC_INPUTPIN, LOW);
  }
  digitalWrite(EC_ENABLEPIN, LOW);
  lowPulseTime = lowPulseTime / EC_SAMPLES;
  highPulseTime = highPulseTime / EC_SAMPLES;
  pulseTime = (lowPulseTime + highPulseTime) / 2 + 2;

  holdingRegs[DATA18] = (int)lowPulseTime;
  holdingRegs[DATA19] = (int)highPulseTime;
  holdingRegs[DATA20] = (int)pulseTime;
  holdingRegs[DATA21] = (int)(100 * calcEC(lowPulseTime, highPulseTime));

  /////////////////////////////////
  // PH
  /////////////////////////////////
  double ph;
  ph = analogRead(PH_INPUTPIN, PH_SAMPLES);
  holdingRegs[DATA22] = int(ph);
  holdingRegs[DATA23] = int(calcPH(ph) * 100);

  double temp;
  temp = analogRead(PHTEMP_INPUTPIN, PH_SAMPLES);
  holdingRegs[DATA24] = int(temp);
  holdingRegs[DATA25] = int(calcPHTemp(temp) * 100);
  
  digitalWrite(LED, LOW);
}

/////////////////////////////////
// EC
/////////////////////////////////

long getHigh(int pin) {
  long pulseTime=0;
  for(unsigned int j=0; j<EC_SAMPLES; j++){
    pulseTime+=pulseIn(pin, HIGH);
  }
  pulseTime= pulseTime/EC_SAMPLES;
  return pulseTime;
}
 
long getLow(int pin) {
  long pulseTime=0;
  for(unsigned int j=0; j<EC_SAMPLES; j++){
    pulseTime+=pulseIn(pin, LOW);
  }
  pulseTime = pulseTime/EC_SAMPLES;
  return pulseTime;
}
  
double calcEC(long lowPulseTime, long highPulseTime) {
  double ec_a, ec_b, ec, pulseTime;
   
  ec_a =  (ECH_SOLUTION - ECL_SOLUTION) / (1/ (double) ECH - 1/ (double)ECL);
  ec_b = ECL_SOLUTION - ec_a / (float) ECL;
  pulseTime = (double)((lowPulseTime + highPulseTime) / 2 + 2);

  ec = (ec_a / pulseTime + ec_b);
  return ec;
}

/////////////////////////////////
// PH
/////////////////////////////////
//double PH7 = EEPROM.read(addrph4);                       // PH7 Buffer Solution Reading.
//double PH4 = EEPROM.read(addrph7); 

double calcPH(double ph) { 
  double phratio = (double)(PH4 - PH7) / (double)(PH7_SOLUTION - PH4_SOLUTION); //move to setup
  //ph = getRawValue(PH_INPUTPIN, PH_SAMPLES)
  ph = ((double)PH7 - ph) / phratio + (double)PH7_SOLUTION;    // Calculate PH
  return ph;
}

double calcPHTemp(double temp) {
  //temp = getRawValue(PHTEMP_INPUTPIN, PH_SAMPLES)
  return temp / 3.4  * (5 / 10.24);   // LM35 connect to CA3140 for amplify 3 time
}



from django.core.management.base import BaseCommand, CommandError
from w.models import Instrument, Rule
import time

import datetime
import time
from time import gmtime, strftime
import sys


import smbus
import time

# i2c address of PCF8574
PCF8574=0x20
# open the bus (0 -- original Pi, 1 -- Rev 2 Pi)
i2c=smbus.SMBus(1)

#import xmpp

#login = 'growmat0000@jabbim.cz' # @gmail.com 
#pwd   = '0000growmat'

#jid = xmpp.protocol.JID(login)
#cl  = xmpp.Client(jid.getDomain())
#if cl.connect(('jabbim.cz',5222)):
#    print 'Jabber: connected'
#    if cl.auth(jid.getNode(), pwd):
#        print 'Jabber: authentication failed'
#    else:
#        print 'Jabber: connectioned failed'
#cl.sendInitPresence()
#cl.send(xmpp.Message( 'growmat@jabbim.cz' ,'GROWMAT ONLINE' ))

#print jid.getNode()
#print jid.getDomain()
#print pwd

from subprocess import call
#call(["ls", "-l"])
import socket
#s = socket.gethostbyname(socket.gethostname())
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(('google.com', 0))
#s = s.getsockname()[0]
#print s
#call('pwd')
call(['python', '/home/pi/xsend.py' ,'growmat@jabbim.cz', 'GROWMAT'])

#import subprocess
from django.utils import timezone

import minimalmodbus
#print minimalmodbus.__file__

station = minimalmodbus.Instrument('/dev/ttyAMA0', 1) # port name, slave address (in decimal)

print station.serial.port          # this is the serial port name
#station.debug = True
station.serial.baudrate = 9600   # Baud
station.serial.bytesize = 8
#station.serial.parity   = serial.PARITY_NONE
station.serial.stopbits = 2
station.serial.timeout  = 0.05   # seconds

#instrument2 = minimalmodbus.Instrument('/dev/ttyAMA0', 2) # port name, slave address (in decimal)
#print instrument2.serial.port          # this is the serial port name
#instrument2.debug = True
#instrument2.serial.baudrate = 9600   # Baud
#instrument2.serial.bytesize = 8
#instrument2.serial.parity   = serial.PARITY_NONE
#instrument2.serial.stopbits = 2
#instrument2.serial.timeout  = 0.05   # seconds

#HUMI0 = 0
#HIND0 = 0
#subprocess.Popen(["python", "archive.py"])

def modbus_read(instrument, s):
        #dinstrument = Instrument.objects.get(pk=9)
		#instrument.address, instrument.type + instrument.index)
                
        #instrument.datetime = datetime.datetime.now()
        #print dinstrument.data_datetime
        #dinstrument.insrument_name = 'kuchyn'
        #print dinstrument.insrument_name
        #dinstrument.save()
        try:
            
            #print datetime.datetime.now()
            #print 'ctu'
            #TEMP0 = station.read_register(1, 0) # Registernumber, number of decimals
            #print 'temperature [C]: ' + str(TEMP0 )
            #print 'do db'			
            #dinstrument.data_value = int(TEMP0)
            #print 
            instrument.status = instrument.status & ~Instrument.NT
            
            station.address = instrument.address
            #print station.address
            value = station.read_register(instrument.type + instrument.index, 0)
            if value == 0:#sys.maxint:
                instrument.status = instrument.status | Instrument.IV
                
            else:   
                instrument.status = instrument.status & ~Instrument.IV         
                #instrument.value = value / 1000 #minimalmodbus._bytestringToFloat(registerstring)
                instrument.value = float(value) * 0.01
            
            instrument.datetime = timezone.now()
            #instrument.status = instrument.status ^ Instrument.INI
            
            instrument.save()
        except:
            instrument.datetime = timezone.now()
            instrument.status = instrument.status | Instrument.NT
            instrument.save()
            #print 'sensor n/a'
            #s.stdout.write('sensor does not response, address {}'.format(instrument.address))
        #instrument.save()
    
    
    

class Command(BaseCommand):

    help = 'Does some magical work'

    def handle(self, *args, **options):
        """ Do your work here """
        
        while 1:
            
            
            instruments = Instrument.objects.order_by('pk')
            #self.stdout.write('There are {} things!'.format(instruments.count()))
            #print "->"
            for instrument in instruments:
                #print "-->"
                #self.stdout.write('reading address {}'.format(instrument.address))
                #self.stdout.write('reading index {}'.format(instrument.type + instrument.index))
                if instrument.address > 0:
                    modbus_read(instrument,self)
                    #self.stdout.write('status {}'.format(instrument.status))
                if instrument.address == 0:
                    if instrument.type == 0:
                        if instrument.index == 0:
                            #instrument.value = int(time.time())
                            instrument.value = int(strftime("1%H%M%S", gmtime()))
                            instrument.save()
            
            
            
            
            rules = Rule.objects.order_by('pk')
            for rule in rules:
                input_value = Instrument.objects.get(pk=rule.input.pk).value
                operation = rule.operation
                input_parameter = rule.input_parameter
                #calculation = 'if ' + input_value + ' ' + operation + ' ' + parametr + ' : True' 
                #calculation = "if {0} {1} {2}: True".format(input_value, operation, parameter)
                #print calculation
                
                if operation == '==':
                    if input_value == input_parameter:
                        rule.result = True
                    else:
                        rule.result = False
                if operation == '!=':
                    if input_value != input_parameter:
                        rule.result = True
                    else:
                        rule.result = False
                if operation == '>':
                    if input_value > input_parameter:
                        rule.result = True
                    else:
                        rule.result = False
                if operation == '<':
                    if input_value < input_parameter:
                        rule.result = True
                    else:
                        rule.result = False
                if operation == '&':
                    if int(input_value) & int(input_parameter):
                        rule.result = True
                    else:
                        rule.result = False
                if operation == '|':
                    if int(input_value) | int(input_parameter):
                        rule.result = True
                    else:
                        rule.result = False
                
                                

                #print rule.description
                if rule.result:
                    if rule.action == '=':
                        #print str(rule.output_parameter)
                        
                        rule.output.value = rule.output_parameter
                        #else:
                        #    rule.output.value = 0
                        rule.output.save()

                
                #rule.result = eval(calculation)
                if rule.result != rule.result0:
                    rule.result0 = rule.result
                    rule.datetime = timezone.now()
                    rule.save()
                    
                    #print str(rule.output.name)
                    #print str(rule.output.address)
                    #print str(rule.output.index)
                    
                    if rule.output.address==0:
                        if rule.output.index==0:
                            #cl.send(xmpp.Message( rule.output.name ,rule.description ))
                            #execfile('python xsend.py "{}" "{}"'.format(rule.output.name ,rule.description))
                            call(['python', '/home/pi/xsend.py' ,'{}'.format(rule.output.name), '{}'.format(rule.description)])
                            print "Jabber: send"
                             
                            
                            
                        
                #print input_value
                #print parameter
                #print rule.result
                #rule.save()
                
            instruments = Instrument.objects.filter(type=10).order_by('pk')			
            
            PCF8574OutputValue = 0xFF
            for instrument in instruments:
                #print "-->"
                #self.stdout.write('reading address {}'.format(instrument.address))
                #self.stdout.write('reading index {}'.format(instrument.type + instrument.index))
                #if instrument.address > 0:
                #    modbus_read(instrument,self)
                #    self.stdout.write('status {}'.format(instrument.status))
                if instrument.address == 0:
                    #if instrument.index == 0:
                        #instrument.value = int(time.time())
                        #instrument.value = int(strftime("1%H%M%S", gmtime()))
                        #instrument.save()
                    if 	instrument.value > 0:
                        PCF8574OutputValue = PCF8574OutputValue ^ (1 << instrument.index)
                    else:
                        PCF8574OutputValue = PCF8574OutputValue | (1 << instrument.index)
                    #print PCF8574OutputValue
                
                
            i2c.write_byte(PCF8574, PCF8574OutputValue)	
            time.sleep(5)

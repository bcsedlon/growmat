from django.core.management.base import BaseCommand
#from django.core.management.base import CommandError
from django.utils import timezone
from django.utils import dateformat
from django.conf import settings

from w.models import Instrument, Rule, Archive

import time
from time import gmtime, strftime

import sys, os
import urllib, re
from subprocess import call

import ConfigParser

import minimalmodbus


#print Archive.objects.raw('DELETE FROM w_archive WHERE 1')

#from django.db import connection
#cursor = connection.cursor()
#cursor.execute('DELETE FROM w_archive WHERE 1')
#connection.commit()
#print '...'



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


#call(["ls", "-l"])

#s = socket.gethostbyname(socket.gethostname())
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(('google.com', 0))
#s = s.getsockname()[0]
#print s
#call('pwd')
#curl -s http://whatismijnip.nl |cut -d " " -f 5

def get_external_ip():
    try:
        site = urllib.urlopen("http://checkip.dyndns.org/").read()
        grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
        address = grab[0]
    except:
        address = '0.0.0.0'    
    return address

#try:
#    fqn = os.uname()[1]
#    ext_ip = urllib2.urlopen('http://whatismyip.org').read()
#    #print ("Asset: %s " % fqn, "Checking in from IP#: %s " % ext_ip)
#except Error:
#    ext_ip = '0.0.0.0'
    

#call(['python', '/home/pi/growmat/xsend.py' ,'growmat@jabbim.cz', 'GROWMAT'])



def modbus_write(station, instrument, s):
    try:
        try:
            station.write_register(instrument.type + instrument.index, instrument.value, 0)
        except:
            station.write_register(instrument.type + instrument.index, instrument.value,  0)
        
        instrument.datetime = timezone.now()
        instrument.status = instrument.status & ~Instrument.cNT
        instrument.save()   
    except:
        instrument.datetime = timezone.now()
        instrument.status = instrument.status | Instrument.cNT
        instrument.save()    

def modbus_read(station, instrument, s):
        try:
            instrument.status = instrument.status & ~Instrument.cNT
            
            station.address = instrument.address
        
            try:
                if instrument.datatype == 0:
                    value = station.read_register(instrument.type + instrument.index, 0)
                    value = value * 0.01
                if instrument.datatype == 1:
                    value = station.read_float(instrument.type + instrument.index, 3)
            except:
                if instrument.datatype == 0:
                    value = station.read_register(instrument.type + instrument.index, 0)
                    value = value * 0.01
                if instrument.datatype == 1:
                    value = station.read_float(instrument.type + instrument.index, 3)
                
            
            if instrument.datatype == 0:
                if value == 32767:#sys.maxint:
                    instrument.status = instrument.status | Instrument.cIV
                else:   
                    instrument.status = instrument.status & ~Instrument.cIV         
                    #instrument.value = value / 1000 #minimalmodbus._bytestringToFloat(registerstring)
                    instrument.value = float(value)
            
            instrument.datetime = timezone.now()
            #instrument.status = instrument.status ^ Instrument.INI
            instrument.save()
            
        except:
            instrument.datetime = timezone.now()
            instrument.status = instrument.status | Instrument.cNT
            instrument.save()
               

class Command(BaseCommand):

    help = 'GROWMAT modbus'

    def handle(self, *args, **options):
        print help
                
        PROJECT_PATH = os.path.dirname(settings.BASE_DIR)
        
        #path = os.path.join(PROJECT_PATH,'growmat','ramdisk', 'raspistill.jpg')
        #os.system('raspistill -v -w 640 -h 480 -vf -s -n -t 0 -o ' + path + ' &') #-tl 60000
        
        #extIP = get_external_ip()
        #text = 'GROWMAT IP: ' + extIP
        text = 'GROWMAT'
        print text
        #call(['python', os.path.join(PROJECT_PATH, 'xsend.py') ,'growmat@jabbim.cz', text])

        Config = ConfigParser.ConfigParser()
        try:
            Config.read(os.path.join(PROJECT_PATH, 'growmat.ini'))
            port = Config.get('modbus', 'port')
            debug = Config.get('modbus', 'debug')
        except:
            cfgfile = open(os.path.join(PROJECT_PATH, 'growmat.ini'),'w+')
            Config.add_section('modbus')
            Config.set('modbus','port','/dev/ttyUSB0')
            #Config.set('modbus','port','/dev/ttyAMA0')
            #Config.set('modbus','port','COM1')
            Config.set('modbus','debug','False')
            
            Config.write(cfgfile)
            cfgfile.close()
            print 'Please check growmat.ini and try again!'
            return
        
        station = minimalmodbus.Instrument(port, 1)

        print station.serial.port          
        if debug == 'True':
            station.debug = True
        
        station.serial.baudrate = 9600   # Baud
        station.serial.bytesize = 8
        #station.serial.parity   = serial.PARITY_NONE
        station.serial.stopbits = 2
        station.serial.timeout  = 0.1
                
        while 1:
            time_now = int(strftime('%H%M%S', gmtime()))
            
            #INPUTS
            print 'inputs'
            instruments = Instrument.objects.order_by('pk')
            for instrument in instruments:
                instrument = Instrument.objects.get(pk=instrument.pk)
                
                if instrument.manual == False and instrument.output == False:
                    if instrument.address > 0:
                        if debug == 'True':
                            print 'read station {} index {}'.format(instrument.address, instrument.index)
                        modbus_read(station, instrument,self)
                    if instrument.address == 0:
                        if instrument.index == 0:
                            instrument.value = int(strftime("%H%M%S", gmtime()))#gmtime()))
                            instrument.save()
            
            #RULES
            print 'rules'
            rules = Rule.objects.order_by('priority')
            for rule in rules:
                print rule.description
                
                time_from =  int(rule.period.time_from.strftime('%H%M%S'))
                time_to =  int(rule.period.time_to.strftime('%H%M%S'))
              
                if time_from < time_now and time_now <= time_to and not rule.output.manual:
                
                    if rule.input_attribute == 'VALUE':                            
                        a = rule.input.value
                    else:
                        a = float(rule.input.status)
                
                    b = rule.input_parameter
                    op = rule.input_operation
                              
                    exp = 'True if {} {} {} else False'.format(a, op, b)
                    r = eval(exp)
                    rule.result = r
              
                    if rule.output_attribute ==  'VALUE':                          
                        a = rule.output.value
                    else:
                        a = rule.output.status
                
                    if rule.result:
                        b = rule.output_parameter_true
                        op = rule.output_action_true
                    else:
                        b = rule.output_parameter_false
                        op = rule.output_action_false
                        
                    if op != 'None':
                        if op == '=':
                            r = b
                        else:
                            if op[0:1] == '&' or op == '|':
                                a = int(a)
                                b = int(b)
                        
                            exp = '{} {} {}'.format(a, op, b)
                            r = eval(exp)
                            if rule.output_attribute == 'VALUE':           
                                rule.output.value = r
                            else:
                                rule.output.status = int(r)
                
                    rule.output.save()
                                
                    
                    if (rule.once and (rule.result != rule.result0)) or ~rule.once:
                        if rule.output.address==0:
                            if rule.output.index==0:
                                #cl.send(xmpp.Message( rule.output.name ,rule.description ))
                                #execfile('python xsend.py "{}" "{}"'.format(rule.output.name ,rule.description))
                                scriptname = os.path.join(PROJECT_PATH, 'xsend.py')
                                #call(['python', '/home/pi/growmat/xsend.py' ,'{}'.format(rule.output.name), '{}'.format(rule.description)])
                                call(['python', scriptname ,'{}'.format(rule.output.name), '{}'.format(rule.description)])
                                #print "Jabber: send"
                        
                            if rule.output.index==1:
                                i = rule.description.find(' ')
                                if i > -1:
                                    scriptparam = ' ' + str(rule.result) + rule.description[i:]
                                    scriptname = os.path.join(PROJECT_PATH, 'growmat', 'scripts', rule.description[:i])
                                else:
                                    scriptparam = ' ' + str(rule.result)
                                    scriptname = os.path.join(PROJECT_PATH, 'growmat', 'scripts', rule.description)
                                                            
                                    scriptname = scriptname + scriptparam + ' &'
                                    #print scriptname + ' start'
                                    print scriptname
                                try:
                                    os.system(scriptname)
                                    #print scriptname + ' end'
                                    #os.spawnl(os.P_DETACH, scriptname)
                                except:
                                    print sys.exc_info()[0]
                    
                    if rule.result != rule.result0:
                        rule.result0 = rule.result
                        rule.datetime = timezone.now()
                        rule.output.status = rule.output.status & ~1
                        rule.save()
                    
                        #fn =  '/home/pi/growmat/growmat/ramdisk/0.csv'
                        fn = os.path.join(PROJECT_PATH, 'growmat', 'ramdisk', '0.csv')
                        f = open(fn, 'a+')
                        f.write(str(rule.id))
                        f.write(';')
                        f.write(dateformat.format(rule.datetime,  'Y-m-d H:i:s'))
                        f.write(';')
                        f.write(str(rule.result))
                        f.write(';')
                        f.write(rule.description)
                        f.write(';')
                        f.write('\n')
                        f.close()

                            
            #OUTPUTS
            print 'outputs'
            instruments = Instrument.objects.filter(output=True).order_by('pk')    
            for instrument in instruments:
                instrument = Instrument.objects.get(pk=instrument.pk)
                
                if instrument.output == True:
                    if instrument.address > 0:
                        if debug=='True':
                            print 'write station {} index {} value {}'.format(instrument.address, instrument.index, instrument.value)
                        modbus_write(station, instrument, self)    	
            
            time.sleep(0.5)

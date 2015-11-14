from django.core.management.base import BaseCommand, CommandError
from w.models import Instrument, Rule, Archive
import time

import datetime
import time
from time import gmtime, strftime

from django.utils import timezone

import os
#import django
#DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
#SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

#print DJANGO_ROOT
#print SITE_ROOT
import datetime
from django.utils import dateformat


class Command(BaseCommand):

    help = 'Does some magical work'

    def handle(self, *args, **options):
        """ Do your work here """
        
        counter = 0
        while 1:
            
            #print timezone.now()
            instruments = Instrument.objects.order_by('pk')
            #self.stdout.write('There are {} things!'.format(instruments.count()))
            #print "->"
            for instrument in instruments:
                #print "-->"
                #self.stdout.write('reading address {}'.format(instrument.address))
                #self.stdout.write('reading index {}'.format(instrument.type + instrument.index))
                fn =  '/home/pi/growmat/growmat/ramdisk/' +   str(instrument.pk) +  '.csv'
                f = open(fn, 'a+')
                f.write(dateformat.format(timezone.now(), 'Y-m-d H:i:s'))
                f.write(';')
                f.write(str(instrument.value))
                f.write(';')
                f.write(str(instrument.status))
                f.write(';')
                f.write('\n')
                f.close()
                
                #archive = Archive()
                #archive.instrument = instrument
                #archive.value = instrument.value
                #archive.status = instrument.status
                #archive.datetime = timezone.now()
                #archive.save()
                
                
            
                
            counter = counter + 1
            if counter > 60:
                counter = 0
                os.system('/home/pi/growmat/garchive')
            time.sleep(60)
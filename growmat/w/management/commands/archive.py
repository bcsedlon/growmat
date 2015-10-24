from django.core.management.base import BaseCommand, CommandError
from w.models import Instrument, Rule, Archive
import time

import datetime
import time
from time import gmtime, strftime

from django.utils import timezone





class Command(BaseCommand):

    help = 'Does some magical work'

    def handle(self, *args, **options):
        """ Do your work here """
        
        while 1:
            
            print timezone.now()
            instruments = Instrument.objects.order_by('pk')
            #self.stdout.write('There are {} things!'.format(instruments.count()))
            #print "->"
            for instrument in instruments:
                #print "-->"
                #self.stdout.write('reading address {}'.format(instrument.address))
                #self.stdout.write('reading index {}'.format(instrument.type + instrument.index))
                archive = Archive()
                archive.instrument = instrument
                archive.value = instrument.value
                archive.status = instrument.status
                archive.datetime = timezone.now()
                archive.save()
                
            
            
            
 
            time.sleep(60)
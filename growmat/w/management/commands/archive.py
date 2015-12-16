from django.core.management.base import BaseCommand, CommandError
from w.models import Instrument, Rule, Archive
import time

import datetime
import time
from time import gmtime, strftime

from django.utils import timezone
from django.conf import settings

import fnmatch
import os
PROJECT_PATH = os.path.dirname(settings.BASE_DIR)


#import django
#DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
#SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

#print DJANGO_ROOT
#print SITE_ROOT
import datetime
from django.utils import dateformat



def appendArchive(srcFilename, dstFilename, delete = False):
    #print srcFilename + ' -> ' + dstFilename
    
    
    with open(dstFilename, 'a+') as dstFile:
        with open(srcFilename) as srcFile:
            for line in srcFile:
                dstFile.write(line)
    if delete:
        os.remove(srcFilename)
    return 0

def appendArchives():
    #path = os.path.join(PROJECT_PATH, 'growmat', 'archives', str(pk), '')
    
    #print path
    #if pk is None:
    #    pk = '*'
    
    #f = []
    srcPath = os.path.join(PROJECT_PATH, 'growmat', 'ramdisk', '')
    dstPath = os.path.join(PROJECT_PATH, 'growmat', 'archives', '') 
    
    
    for file in os.listdir(srcPath):
        if fnmatch.fnmatch(file, '*.csv'):
            pk, extension = os.path.splitext(file)
            if not os.path.exists(os.path.join(dstPath, pk)):
                os.mkdir(os.path.join(dstPath, pk))
                
            d = time.strftime('%Y%m%d-')    
            appendArchive(os.path.join(srcPath, file),  os.path.join(dstPath, pk, d + file), True)
            #f.append(file)
            
    
    
    return 0


class Command(BaseCommand):

    help = 'Does some magical work'

    def handle(self, *args, **options):
        """ Do your work here """
        
        print 'GROWMAT archive'
        
        #appendArchives()
        #return
        
        
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
                
                
                fn =  os.path.join(PROJECT_PATH,'growmat', 'ramdisk', str(instrument.pk) +  '.csv')
                #print fn
                #fn =  '/home/pi/growmat/growmat/ramdisk/' +   str(instrument.pk) +  '.csv'
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
                
                
            
            minute = dateformat.format(timezone.now(), 'i')
            #counter = counter + 1
            #if counter > 60:
            #    counter = 0
            if minute == '00':
                #NOT WORK ON WINDOWS, has to be rewrite to python
                #os.system('/home/pi/growmat/garchive')
                appendArchives()
            time.sleep(60)
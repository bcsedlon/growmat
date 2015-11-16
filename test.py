import os
import fnmatch    
    
path = '/home/pi/growmat/archives'

pk = None
#pk = 1 
if pk is None:
    pk = '*'
    
for file in os.listdir(path):
        if fnmatch.fnmatch(file, '*-' + str(pk) + '.csv'):
            print file





from ftplib import FTP
import urllib2
import time
import io
import sys,os
from django.db.backends.oracle.creation import PASSWORD


ftpparams={}
#if os.access(os.environ['HOME']+'/.xsend',os.R_OK):
if os.access('/home/pi/growmat/.xftp',os.R_OK):
    #for ln in open(os.environ['HOME']+'/.xsend').readlines():
    for ln in open('/home/pi/growmat/.xftp').readlines():
        if not ln[0] in ('#',';'):
            key,val=ln.strip().split('=',1)
            ftpparams[key.lower()]=val
for mandatory in ['ftpserver','username', 'password']:
    if mandatory not in ftpparams.keys():
        open('/home/pi/growmat/.xftp','w').write('#Uncomment fields before use and type in correct credentials.\n#FTPSERVER=romeo.montague.net\n#USERNAME=romeo@montague.net\n#PASSWORD=juliet\n')
        print 'Please point ~/growmat/.xftp config file to valid FTP .'
        sys.exit(0)
        
#request = ''
#response = ''
#lastts = 0

#def writeFunc(s):
#    global request
#    request = s
    #print "Read: " + s
#print ftpserver
#print username
#print password

while True:
 #print ca.readline()

 try:
    ftp = FTP(ftpparams['ftpserver'])
    ftp.login(ftpparams['username'], ftpparams['password'])
    #ftp.cwd('/Xrouter')
    #ftp.retrbinary('RETR /Xrouter/request.log', writeFunc)

    #print request
    #ts = request[0:request.find('\n')]
    #if ts <> lastts:
    #    lastts = ts
        
        #request = request[request.find('\n')+1:len(request)]
    url = 'http://127.0.0.1/w' 
    response = urllib2.urlopen(url).read()
    #response = response.replace('href="/w','href="/Xrouter/w')
    file = io.BytesIO(response)#.encode("utf-8"))
    ftp.storlines('STOR /w/index.html', file)
    file.close()
        #url = 'http://127.0.0.1' + request
        #print url

    #    response = urllib2.urlopen(url).read()

    #    response = response.replace('href="/w','href="/Xrouter/w')
        #print response

    #    file = io.BytesIO(response)#.encode("utf-8"))

        #import StringIO
        #output = StringIO.StringIO(response)
        #output.write(response)
        #output.getvalue()
        #print output.readline()

     #   a = ftp.storlines('STOR /Xrouter/response.log', file)
        #output.close()
     #   file.close()

        #print a
 except:
	pass
 ftp.quit()
    
 time.sleep(60)

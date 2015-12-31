#!/usr/bin/python
# $Id: xsend.py,v 1.8 2006/10/06 12:30:42 normanr Exp $
import sys,os,xmpp,time

if len(sys.argv) < 2:
    print "Syntax: xsend JID text"
    sys.exit(0)

tojid=sys.argv[1]
text=' '.join(sys.argv[2:])

jidparams={}

PATH = os.path.dirname(__file__)
 
#if os.access(os.environ['HOME']+'/.xsend',os.R_OK):
if os.access(os.path.join(PATH, '.xsend'), os.R_OK):
    #for ln in open(os.environ['HOME']+'/.xsend').readlines():
    for ln in open(os.path.join(PATH, '.xsend')).readlines():
        if not ln[0] in ('#',';'):
            key,val=ln.strip().split('=',1)
            jidparams[key.lower()]=val
for mandatory in ['jid','password']:
    if mandatory not in jidparams.keys():
        #open(os.environ['HOME']+'/.xsend','w').write('#Uncomment fields before use and type in correct credentials.\n#JID=romeo@montague.net/resource (/resource is optional)\n#PASSWORD=juliet\n')
        open(os.path.join(PATH, '.xsend'),'w').write('#Uncomment fields before use and type in correct credentials.\n#JID=romeo@montague.net/resource (/resource is optional)\n#PASSWORD=juliet\n')
        print 'Please point ' + os.path.join(PATH, '.xsend') + ' config file to valid JID for sending messages.'
        sys.exit(0)

jid=xmpp.protocol.JID(jidparams['jid'])
cl=xmpp.Client(jid.getDomain(),debug=[])

#print jid.getDomain()
#server=('talk.google.com', 5223)
server=(jid.getDomain(), 5223)
con=cl.connect(server)
if not con:
    #print 'could not connect!'
    sys.exit()
#print 'connected with',con

#print jid.getNode()
#print jidparams['password']
#print jid.getResource()

#print tojid
#print text

auth=cl.auth(jid.getNode(),jidparams['password'],resource=jid.getResource())
if not auth:
    #print 'could not authenticate!'
    sys.exit()
#print 'authenticated using',auth

#cl.SendInitPresence(requestRoster=0)   # you may need to uncomment this for old server
id=cl.send(xmpp.protocol.Message(tojid,text))
#print 'sent message with id',id

time.sleep(1)   # some older servers will not send the message if you disconnect immediately after sending

#cl.disconnect()
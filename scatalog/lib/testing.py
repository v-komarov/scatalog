#!/usr/bin/python
#coding:utf-8

import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary



srv=Client(server="10.6.0.250", secret="secretttk",dict=Dictionary("dictionary", "dictionary.acc"))
      
req=srv.CreateAuthPacket(code=pyrad.packet.AccessRequest,User_Name='VKomarov', NAS_Identifier="scatalog")
req["User-Password"]=req.PwCrypt('82269021')
                    
reply=srv.SendPacket(req)
if reply.code==pyrad.packet.AccessAccept:
    print reply['Reply-Message']    
    print "access accepted"
else:
    print "access denied"
                            
print "Attributes returned by server:"
for i in reply.keys():
    print "%s: %s" % (i, reply[i])


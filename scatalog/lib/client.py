#!/usr/bin/python
#coding:utf-8

import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary



def AuthUser(login,password,request):


    srv=Client(server="10.6.0.250", secret="secretttk",dict=Dictionary("scatalog/lib/dictionary", "scatalog/lib/dictionary.acc"))
      
    req=srv.CreateAuthPacket(code=pyrad.packet.AccessRequest,User_Name=login.encode('utf-8'), NAS_Identifier="scatalog")
    req["User-Password"]=req.PwCrypt(password.encode('utf-8'))

    reply=srv.SendPacket(req)
    if reply.code==pyrad.packet.AccessAccept:
	request.session['key777'] = reply['Reply-Message']
	print "access accepted"
	return "access accepted"
    else:
	return "access denied"
        print "access denied"                    
    print "Attributes returned by server:"
    for i in reply.keys():
	print "%s: %s" % (i, reply[i])


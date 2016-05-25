#coding:utf-8
from django.shortcuts import render


from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	scatalog.lib.userdata	import	GetUserKod,CheckAccess,GetFio


import	pickle


def	Reports(request):


    try:
	if CheckAccess(request,'24') != 'OK':
	    return render_to_response("client/notaccess/clientlist.html")
    except:
	return HttpResponseRedirect('/')




    c = RequestContext(request,{})
    c.update(csrf(request))
    return render_to_response("client/reports.html",c)



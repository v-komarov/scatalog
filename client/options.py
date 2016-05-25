#coding:utf-8
from django.shortcuts import render


from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	scatalog.lib.userdata	import	GetUserKod,CheckAccess,GetFio
from	forms	import	AddEmailForm
from	scatalog.lib.clients	import	AddEmailUser,GetEmailUser,DelEmailUser


import	pickle


def	Options(request):


    try:
	if CheckAccess(request,'25') != 'OK':
	    return render_to_response("client/notaccess/options.html")
    except:
	return HttpResponseRedirect('/')

    form = AddEmailForm(request.POST)
    if form.is_valid():
	status = form.cleaned_data['status']
	user = form.cleaned_data['user']
	AddEmailUser( request,
	    user,
	    status
	    )

    if request.method == 'GET':

	try:
	    delemail = request.GET['delemail']
	    DelEmailUser(delemail)
	except:
	    pass



    data = GetEmailUser()

    form = AddEmailForm(None)


    c = RequestContext(request,{'form':form,'data':data})
    c.update(csrf(request))
    return render_to_response("client/options.html",c)



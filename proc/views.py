#coding:utf-8
from django.shortcuts import render


from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	scatalog.lib.userdata	import	GetUserKod,CheckAccess
from	scatalog.lib.proc	import	NewProc,GetProcList,GetProc,SaveProcData,ListFile,AddComment,GetCommentList,DelComment,NextPerson,PointStep,ListStepHistory,GetAttrs,AddAttr,GetAttrList,DelAttr
from	scatalog.lib.proc_mail	import	SendNextPerson,SendComment,ProcOver
from	forms			import	ProcForm,CommentForm,StepForm,AttrForm

import	pickle


def	ProcList(request):

    try:
	if CheckAccess(request,'6') != 'OK':
	    return render_to_response("proc/notaccess/proc.html")
    except:
	return HttpResponseRedirect('/')



    ### --- Получение номера страницы ---
    try:
	page = request.GET['page']
	request.session['page'] = page
    except:
	pass
	
    try:
	page = request.session['page']
    except:
	page = '1'


    data = GetProcList()


    paginator = Paginator(data,50)
    try:
	data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
	data_page = paginator.page(paginator.num_pages)


    c = RequestContext(request,{'data':data_page})
    c.update(csrf(request))
    return render_to_response("proc/proclist.html",c)








def	ProcData(request):

    try:
	if CheckAccess(request,'6') != 'OK':
	    return render_to_response("proc/notaccess/proc.html")
    except:
	return HttpResponseRedirect('/')

    if request.method == 'GET':
	try:
	    proc_id = request.GET['proc_id']
	    if proc_id == 'new':
		proc_id = NewProc(request)
	    request.session['proc_id'] = proc_id
	except:
	    pass

    proc_id = request.session['proc_id']

    proc = GetProc(proc_id)

    if request.method == 'POST':
	form = ProcForm(request.POST)
	if form.is_valid() and proc['author'] == GetUserKod(request):
	    status = form.cleaned_data['status']
	    name = form.cleaned_data['name']
	    scheme = form.cleaned_data['scheme']
	    info = form.cleaned_data['info']
	    SaveProcData(request,proc_id,name,scheme,status,info)
	    ### --- Если сохраняем и статус "Выполнение" то делаем уведомление следубщему согласующему ---
	    SendNextPerson(request,proc_id)

    proc = GetProc(proc_id)

    form = ProcForm(None)
    form.fields['status'].initial = proc['status']
    form.fields['name'].initial = proc['proc_name']
    form.fields['scheme'].initial = proc['scheme_link']
    form.fields['info'].initial = proc['info']

    author = proc['author_name'].split()[1]+u' '+proc['author_name'].split()[0]

    c = RequestContext(request,{'proc':proc_id,'form':form,'status':proc['status'],'name':proc['proc_name'],'author':author})
    c.update(csrf(request))
    return render_to_response("proc/procdata.html",c)








### --- Согласования ---
def	ProcStep(request):

    try:
	if CheckAccess(request,'6') != 'OK':
	    return render_to_response("proc/notaccess/proc.html")
    except:
	return HttpResponseRedirect('/')


    proc_id = request.session['proc_id']

    next_person = NextPerson(proc_id)
    proc = GetProc(proc_id)

    if request.method == 'POST':
	form = StepForm(request.POST)
	if form.is_valid() and next_person['kod'] == GetUserKod(request) and proc['status'] == u'Выполняется':
	    yesno = form.cleaned_data['yesno']
	    comment = form.cleaned_data['comment']
	    result = PointStep(proc_id,yesno,comment,next_person)
	    SendNextPerson(request,proc_id)
	    if result == 'OVER':
		### -- Уведомление о завершении ---
		ProcOver(proc_id)


    proc = GetProc(proc_id)

    form = StepForm(None)

    author = proc['author_name'].split()[1]+u' '+proc['author_name'].split()[0]

    data = ListStepHistory(proc_id)
    c = RequestContext(request,{'form':form,'proc':proc_id,'status':proc['status'],'name':proc['proc_name'],'author':author,'nextperson':next_person,'data':data})
    c.update(csrf(request))
    return render_to_response("proc/procstep.html",c)







### --- Комментарии и приложения ---
def	ProcComment(request):

    try:
	if CheckAccess(request,'6') != 'OK':
	    return render_to_response("proc/notaccess/proc.html")
    except:
	return HttpResponseRedirect('/')

    if request.method == 'GET':
	try:
	    proc_id = request.GET['proc_id']
	    request.session['proc_id'] = proc_id
	except:
	    pass

    proc_id = request.session['proc_id']


    try:
	comment_id = request.GET['comment_delete']
	DelComment(proc_id,comment_id,request)
    except:
	pass


    if request.method == 'POST':
	form = CommentForm(request.POST)
	if form.is_valid():
	    file_link = form.cleaned_data['file_link']
	    comment = form.cleaned_data['comment']
	    if file_link == '':
		file_link = '#'
	    AddComment(proc_id,file_link.split('#')[0],file_link.split('#')[1],comment,request)
	    SendComment(request,proc_id,comment,file_link)


    form = CommentForm(None)
    filelist = ListFile(GetUserKod(request))
    filelist.insert(0,['',''])
    form.fields['file_link'].choices = filelist

    proc = GetProc(proc_id)

    data = GetCommentList(proc_id)

    author = proc['author_name'].split()[1]+u' '+proc['author_name'].split()[0]

    c = RequestContext(request,{'form':form,'proc':proc_id,'data':data,'status':proc['status'],'name':proc['proc_name'],'author':author})
    c.update(csrf(request))
    return render_to_response("proc/proccomment.html",c)






### --- История уведомлений ---
def	ProcEmail(request):

    try:
	if CheckAccess(request,'6') != 'OK':
	    return render_to_response("proc/notaccess/proc.html")
    except:
	return HttpResponseRedirect('/')

    if request.method == 'GET':
	try:
	    proc_id = request.GET['proc_id']
	    request.session['proc_id'] = proc_id
	except:
	    pass

    proc_id = request.session['proc_id']

    proc = GetProc(proc_id)
    data = pickle.loads(proc['email_data'])
    data.reverse()

    author = proc['author_name'].split()[1]+u' '+proc['author_name'].split()[0]

    c = RequestContext(request,{'proc':proc_id,'status':proc['status'],'name':proc['proc_name'],'author':author,'data':data})
    c.update(csrf(request))
    return render_to_response("proc/procemail.html",c)






### --- Все файлы по процессу ---
def	ProcFiles(request):

    try:
	if CheckAccess(request,'6') != 'OK':
	    return render_to_response("proc/notaccess/proc.html")
    except:
	return HttpResponseRedirect('/')

    if request.method == 'GET':
	try:
	    proc_id = request.GET['proc_id']
	    request.session['proc_id'] = proc_id
	except:
	    pass

    proc_id = request.session['proc_id']

    proc = GetProc(proc_id)
    data = GetCommentList(proc_id)
    

    author = proc['author_name'].split()[1]+u' '+proc['author_name'].split()[0]

    c = RequestContext(request,{'proc':proc_id,'status':proc['status'],'name':proc['proc_name'],'author':author,'data':data})
    c.update(csrf(request))
    return render_to_response("proc/procfiles.html",c)





### --- Атрибуты ---
def	ProcAttrs(request):

    try:
	if CheckAccess(request,'6') != 'OK':
	    return render_to_response("proc/notaccess/proc.html")
    except:
	return HttpResponseRedirect('/')


    proc_id = request.session['proc_id']

    proc = GetProc(proc_id)

    try:
	attr_id = request.GET['attr_delete']
	DelAttr(proc_id,attr_id)
    except:
	pass


    if request.method == 'POST':
	form = AttrForm(request.POST)
	if form.is_valid():
	    attr = form.cleaned_data['attr']
	    value = form.cleaned_data['value']
	    AddAttr(proc_id,attr,value,request)

    form = AttrForm(None)
    form.fields['attr'].choices = GetAttrs(proc_id)

    author = proc['author_name'].split()[1]+u' '+proc['author_name'].split()[0]

    data = GetAttrList(proc_id)
    c = RequestContext(request,{'form':form,'proc':proc_id,'status':proc['status'],'name':proc['proc_name'],'author':author,'data':data})
    c.update(csrf(request))
    return render_to_response("proc/procattrs.html",c)


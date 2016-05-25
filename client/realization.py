#coding:utf-8
from django.shortcuts import render


from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField, BooleanField

from	scatalog.lib.userdata	import	GetUserKod,CheckAccess,GetFio
from	scatalog.lib.clients	import	NewClient,GetList,GetClient,ClientEdit,ListFile,GetTech,TechEdit,AddTechFile,GetTechFiles,DelTechFile,GetCom,ComEdit,AddComFile,GetComFiles,DelComFile,AddOrderFile,GetOrderFiles,BuildEdit,AddRealFile,GetRealFiles,DelRealFile,ConfigEdit,UTPEdit,InReal
from	forms			import	RealBuildForm,FileForm,RealConfigForm,RealUTPForm
from	scatalog.lib.clients_status	import	StatusHistory


import	pickle





def	RealBuild(request):
    
    try:
	client_id = request.session['client_id']
    except:
	return HttpResponseRedirect('/clientlist')


    if request.method == 'POST':

	try:
	    file_link = request.POST['file_link']
	    if file_link != '':
		AddRealFile('build',client_id,file_link)
	except:
	    pass

	form = RealBuildForm(request.POST)
	if form.is_valid():
	    smartasr_order = form.cleaned_data['smartasr_order']
	    date_order = form.cleaned_data['date_order']
	    date_tmc = form.cleaned_data['date_tmc']
	    date_doc = form.cleaned_data['date_doc']
	    date_tmc_out = form.cleaned_data['date_tmc_out']
	    date_end = form.cleaned_data['date_end']
	    sz = form.cleaned_data['sz']
	    iss = form.cleaned_data['iss']
	    date_real = form.cleaned_data['date_real']
	    date_realend = form.cleaned_data['date_realend']
	    comment = form.cleaned_data['comment']

	    a = GetFio(request)
	    author = a.split()[1]+' '+a.split()[0]

	    BuildEdit( client_id,smartasr_order,date_order,
		date_tmc, date_doc, date_tmc_out, date_end, sz, iss,
		date_real, date_realend, comment, author
		)
	    StatusHistory(client_id,'Реализация',request)


    if request.method == 'GET':

	try:
	    delete_file = request.GET['delete_file']
	    DelRealFile('build',client_id,delete_file)
	except:
	    pass

	try:
	    in_real = request.GET['in_real']
	    InReal(request,client_id)
	    StatusHistory(client_id,'Принято в реализацию',request)
	except:
	    pass


    field = DateTimeField()

    client = GetClient(client_id)
    creator = client['creator_name'].split()[1]+' '+client['creator_name'].split()[0]
    create = field._to_python(client['create'])

    real = pickle.loads(client['realization_data'])
    build = real['build']

    form = RealBuildForm(None)    
    form.fields['smartasr_order'].initial = build['smartasr_order']
    form.fields['date_order'].initial = build['date_order']
    form.fields['date_tmc'].initial = build['date_tmc']
    form.fields['date_doc'].initial = build['date_doc']
    form.fields['date_tmc_out'].initial = build['date_tmc_out']
    form.fields['date_end'].initial = build['date_end']
    form.fields['sz'].initial = build['sz']
    form.fields['iss'].initial = build['iss']
    form.fields['date_real'].initial = build['date_real']
    form.fields['date_realend'].initial = build['date_realend']
    form.fields['comment'].initial = build['comment']

    fform = FileForm(None)
    filelist = ListFile(GetUserKod(request))
    filelist.insert(0,['',''])
    fform.fields['file_link'].choices = filelist

    #--- Список файлов ---
    realfiles = GetRealFiles('build',client_id)

    c = RequestContext(request,{'fform':fform,'form':form,'client':client,'creator':creator,'create':create,'realfiles':realfiles})
    c.update(csrf(request))
    return render_to_response("client/build.html",c)








def	RealConfig(request):
    
    try:
	client_id = request.session['client_id']
    except:
	return HttpResponseRedirect('/clientlist')



    if request.method == 'POST':

	try:
	    file_link = request.POST['file_link']
	    if file_link != '':
		AddRealFile('config',client_id,file_link)
	except:
	    pass


	form = RealConfigForm(request.POST)
	if form.is_valid():
	    smartasr_order = form.cleaned_data['smartasr_order']
	    date_order = form.cleaned_data['date_order']
	    sz = form.cleaned_data['sz']
	    date_real = form.cleaned_data['date_real']
	    date_realend = form.cleaned_data['date_realend']
	    comment = form.cleaned_data['comment']

	    a = GetFio(request)
	    author = a.split()[1]+' '+a.split()[0]

	    ConfigEdit( client_id, smartasr_order, date_order,
		sz, date_real, date_realend,
		comment, author
		)
	    StatusHistory(client_id,'Реализация',request)


    if request.method == 'GET':

	try:
	    delete_file = request.GET['delete_file']
	    DelRealFile('config',client_id,delete_file)
	except:
	    pass

	try:
	    in_real = request.GET['in_real']
	    InReal(request,client_id)
	    StatusHistory(client_id,'Принято в реализацию',request)
	except:
	    pass



    field = DateTimeField()

    client = GetClient(client_id)
    creator = client['creator_name'].split()[1]+' '+client['creator_name'].split()[0]
    create = field._to_python(client['create'])

    real = pickle.loads(client['realization_data'])
    config = real['config']

    form = RealConfigForm(None)    
    form.fields['smartasr_order'].initial = config['smartasr_order']
    form.fields['date_order'].initial = config['date_order']
    form.fields['sz'].initial = config['sz']
    form.fields['date_real'].initial = config['date_real']
    form.fields['date_realend'].initial = config['date_realend']
    form.fields['comment'].initial = config['comment']

    fform = FileForm(None)
    filelist = ListFile(GetUserKod(request))
    filelist.insert(0,['',''])
    fform.fields['file_link'].choices = filelist

    #--- Список файлов ---
    realfiles = GetRealFiles('config',client_id)

    c = RequestContext(request,{'fform':fform,'form':form,'client':client,'creator':creator,'create':create,'realfiles':realfiles})
    c.update(csrf(request))
    return render_to_response("client/config.html",c)






def	RealUTP(request):
    
    try:
	client_id = request.session['client_id']
    except:
	return HttpResponseRedirect('/clientlist')


    if request.method == 'POST':

	try:
	    file_link = request.POST['file_link']
	    if file_link != '':
		AddRealFile('utp',client_id,file_link)
	except:
	    pass

	form = RealUTPForm(request.POST)
	if form.is_valid():
	    smartasr_order = form.cleaned_data['smartasr_order']
	    date_order = form.cleaned_data['date_order']
	    iss = form.cleaned_data['iss']
	    date_real = form.cleaned_data['date_real']
	    date_realend = form.cleaned_data['date_realend']
	    comment = form.cleaned_data['comment']

	    a = GetFio(request)
	    author = a.split()[1]+' '+a.split()[0]

	    UTPEdit( client_id, smartasr_order, date_order,
		iss, date_real, date_realend,
		comment, author
		)
	    StatusHistory(client_id,'Реализация',request)


    if request.method == 'GET':

	try:
	    delete_file = request.GET['delete_file']
	    DelRealFile('utp',client_id,delete_file)
	except:
	    pass

	try:
	    in_real = request.GET['in_real']
	    InReal(request,client_id)
	    StatusHistory(client_id,'Принято в реализацию',request)
	except:
	    pass



    field = DateTimeField()

    client = GetClient(client_id)
    creator = client['creator_name'].split()[1]+' '+client['creator_name'].split()[0]
    create = field._to_python(client['create'])

    real = pickle.loads(client['realization_data'])
    utp = real['utp']

    form = RealUTPForm(None)
    form.fields['smartasr_order'].initial = utp['smartasr_order']
    form.fields['date_order'].initial = utp['date_order']
    form.fields['iss'].initial = utp['iss']
    form.fields['date_real'].initial = utp['date_real']
    form.fields['date_realend'].initial = utp['date_realend']
    form.fields['comment'].initial = utp['comment']

    fform = FileForm(None)
    filelist = ListFile(GetUserKod(request))
    filelist.insert(0,['',''])
    fform.fields['file_link'].choices = filelist

    #--- Список файлов ---
    realfiles = GetRealFiles('utp',client_id)

    c = RequestContext(request,{'fform':fform,'form':form,'client':client,'creator':creator,'create':create,'realfiles':realfiles})
    c.update(csrf(request))
    return render_to_response("client/utp.html",c)


#coding:utf-8
from django.shortcuts import render


from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField, BooleanField

from	scatalog.lib.userdata	import	GetUserKod,CheckAccess
from	scatalog.lib.clients	import	NewClient,GetList,GetClient,ClientEdit,ListFile,GetTech,TechEdit,AddTechFile,GetTechFiles,DelTechFile,GetCom,ComEdit,AddComFile,GetComFiles,DelComFile,AddOrderFile,GetOrderFiles,DelOrderFile,ComOk,GetEmailHistory,InWork
from	forms			import	OrderForm,TechnicalForm,FileForm,CommercialForm,SearchForm
from	realization		import	RealBuild
from	scatalog.lib.clients_status	import	StatusHistory,GetStatusHistory


import	pickle


def	List(request):

    try:
	if CheckAccess(request,'24') != 'OK':
	    return render_to_response("client/notaccess/clientlist.html")
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


    try:
	search = request.session['search']
    except:
	search = ''

    if request.method == 'POST':
	
	form = SearchForm(request.POST)
	if form.is_valid():
	    search = form.cleaned_data['search']
	    request.session['search'] = search




    data = GetList(search)


    paginator = Paginator(data,50)
    try:
	data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
	data_page = paginator.page(paginator.num_pages)

    form = SearchForm(None)
    form.fields['search'].initial = search

    c = RequestContext(request,{'form':form,'data':data_page})
    c.update(csrf(request))
    return render_to_response("client/clientlist.html",c)






### -- Новый запрос на подключение ---
def	New(request):


    try:
	if CheckAccess(request,'24') != 'OK':
	    return render_to_response("client/notaccess/clientlist.html")
    except:
	return HttpResponseRedirect('/')

    if request.method == 'POST':
	form = OrderForm(request.POST)
	if form.is_valid():
	    priority = form.cleaned_data['priority']
	    name = form.cleaned_data['name']
	    address = form.cleaned_data['address']
	    inn = form.cleaned_data['inn']
	    product = form.cleaned_data['product']
	    point = form.cleaned_data['point']
#	    manager = form.cleaned_data['manager']
	    service = form.cleaned_data['service']
	    speed = form.cleaned_data['speed']
	    interface = form.cleaned_data['interface']
	    option = form.cleaned_data['option']
	    client = form.cleaned_data['client']
	    email = form.cleaned_data['email']
	    phone = form.cleaned_data['phone']
	    result = NewClient( request, priority,
		name, address, inn,
		product, point, 
		service, speed, interface,
		option, client, email, phone
		)
	    if result:
		StatusHistory(result,'Запрос',request)
		return HttpResponseRedirect('/clientlist')

    form = OrderForm(None)

    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("client/clientnew.html",c)




### --- Основной интерфейс ---
def	Client(request):

    try:
	if CheckAccess(request,'24') != 'OK':
	    return render_to_response("client/notaccess/clientlist.html")
    except:
	return HttpResponseRedirect('/')


    if request.method == 'GET':
	try:
	    client_id = request.GET['client_id']
	    request.session['client_id'] = client_id 
	except:
	    pass

    try:
	client_id = request.session['client_id']
    except:
	return HttpResponseRedirect('/clientlist')



    if request.method == 'POST':

	try:
	    file_link = request.POST['file_link']
	    if file_link != '':
		AddOrderFile(client_id,file_link)
	except:
	    pass

	form = OrderForm(request.POST)
	if form.is_valid():
	    priority = form.cleaned_data['priority']
	    name = form.cleaned_data['name']
	    address = form.cleaned_data['address']
	    inn = form.cleaned_data['inn']
	    product = form.cleaned_data['product']
	    point = form.cleaned_data['point']
#	    manager = form.cleaned_data['manager']
	    service = form.cleaned_data['service']
	    speed = form.cleaned_data['speed']
	    interface = form.cleaned_data['interface']
	    option = form.cleaned_data['option']
	    client = form.cleaned_data['client']
	    email = form.cleaned_data['email']
	    phone = form.cleaned_data['phone']
	    ClientEdit( client_id, priority,
		name, address, inn,
		product, point, 
		service, speed, interface,
		option, client, email, phone
		)
	    StatusHistory(client_id,'Запрос',request)


    if request.method == 'GET':

	try:
	    delete_file = request.GET['delete_file']
	    DelOrderFile(client_id,delete_file)
	except:
	    pass

	try:
	    in_work = request.GET['in_work']
	    InWork(request,client_id)
	    StatusHistory(client_id,'Принято в работу',request)
	except:
	    pass



    client = GetClient(client_id)


    form = OrderForm(None)
    form.fields['priority'].initial = client['priority']
    form.fields['name'].initial = client['name']
    form.fields['address'].initial = client['address']
    form.fields['inn'].initial = client['inn']
    form.fields['product'].initial = client['product']
    form.fields['point'].initial = client['point']
#    form.fields['manager'].initial = client['manager_kod']
    form.fields['service'].initial = client['service']
    form.fields['speed'].initial = client['speed']
    form.fields['interface'].initial = client['interface']
    form.fields['option'].initial = client['option']
    form.fields['client'].initial = client['client']
    form.fields['email'].initial = client['email']
    form.fields['phone'].initial = client['phone']

    field = DateTimeField()

    creator = client['creator_name'].split()[1]+' '+client['creator_name'].split()[0]
    create = field._to_python(client['create'])


    fform = FileForm(None)
    filelist = ListFile(GetUserKod(request))
    filelist.insert(0,['',''])
    fform.fields['file_link'].choices = filelist

    #--- Список файлов ---
    orderfiles = GetOrderFiles(client_id)

    c = RequestContext(request,{'form':form,'client':client,'creator':creator,'create':create,'fform':fform,'orderfiles':orderfiles})
    c.update(csrf(request))
    return render_to_response("client/client.html",c)






### --- Техническое решение ---
def	Technical(request):

    try:
	if CheckAccess(request,'24') != 'OK':
	    return render_to_response("client/notaccess/clientlist.html")
    except:
	return HttpResponseRedirect('/')


    try:
	client_id = request.session['client_id']
    except:
	return HttpResponseRedirect('/clientlist')



    if request.method == 'POST':

	try:
	    file_link = request.POST['file_link']
	    if file_link != '':
		AddTechFile(client_id,file_link)
	except:
	    pass

	form = TechnicalForm(request.POST)
	if form.is_valid():
	    use = form.cleaned_data['use']
	    onepay = form.cleaned_data['onepay']
	    monthpay = form.cleaned_data['monthpay']
	    option = form.cleaned_data['option']
	    jobokp = form.cleaned_data['jobokp']
	    nemis = form.cleaned_data['nemis']
	    comment = form.cleaned_data['comment']
	    TechEdit( client_id,
		use, onepay, monthpay,
		option, jobokp, nemis, comment
		)
	    StatusHistory(client_id,'Техническое решение',request)




    if request.method == 'GET':

	try:
	    delete_file = request.GET['delete_file']
	    DelTechFile(client_id,delete_file)
	except:
	    pass

    client = GetClient(client_id)

    tech = GetTech(client_id)

    form = TechnicalForm(None)
    form.fields['use'].initial = tech['use']
    form.fields['onepay'].initial = tech['onepay']
    form.fields['monthpay'].initial = tech['monthpay']
    form.fields['option'].initial = tech['option']
    form.fields['jobokp'].initial = tech['jobokp']
    form.fields['nemis'].initial = tech['nemis']
    form.fields['comment'].initial = tech['comment']
    fform = FileForm(None)
    filelist = ListFile(GetUserKod(request))
    filelist.insert(0,['',''])
    fform.fields['file_link'].choices = filelist

    field = DateTimeField()

    creator = client['creator_name'].split()[1]+' '+client['creator_name'].split()[0]
    create = field._to_python(client['create'])

    #--- Список файлов ---
    techfiles = GetTechFiles(client_id)

    c = RequestContext(request,{'form':form,'fform':fform,'client':client,'creator':creator,'create':create,'techfiles':techfiles,'nemis':tech['nemis']})
    c.update(csrf(request))
    return render_to_response("client/technical.html",c)






### --- Коммерческое решение ---
def	Commercial(request):

    try:
	if CheckAccess(request,'24') != 'OK':
	    return render_to_response("client/notaccess/clientlist.html")
    except:
	return HttpResponseRedirect('/')


    try:
	client_id = request.session['client_id']
    except:
	return HttpResponseRedirect('/clientlist')






    if request.method == 'POST':

	try:
	    file_link = request.POST['file_link']
	    if file_link != '':
		AddComFile(client_id,file_link)
	except:
	    pass

	form = CommercialForm(request.POST)
	if form.is_valid():
	    kp = form.cleaned_data['kp']
	    onepay = form.cleaned_data['onepay']
	    monthpay = form.cleaned_data['monthpay']
	    result = form.cleaned_data['result']
	    manager = form.cleaned_data['manager']
	    comment = form.cleaned_data['comment']
	    ComEdit( client_id,
		kp, onepay, monthpay,
		result, manager, comment
		)
	    StatusHistory(client_id,'Коммерческая часть',request)





    if request.method == 'GET':

	try:
	    delete_file = request.GET['delete_file']
	    DelComFile(client_id,delete_file)
	except:
	    pass

	try:
	    ok = request.GET['ok']
	    ComOk(client_id)
	    StatusHistory(client_id,'Согласовано',request)
	except:
	    pass


    client = GetClient(client_id)

    com = GetCom(client_id)

    form = CommercialForm(None)
    form.fields['kp'].initial = com['kp']
    form.fields['onepay'].initial = com['onepay']
    form.fields['monthpay'].initial = com['monthpay']
    form.fields['result'].initial = com['result']
    form.fields['manager'].initial = com['manager']
    form.fields['comment'].initial = com['comment']
    fform = FileForm(None)
    filelist = ListFile(GetUserKod(request))
    filelist.insert(0,['',''])
    fform.fields['file_link'].choices = filelist

    field = DateTimeField()

    creator = client['creator_name'].split()[1]+' '+client['creator_name'].split()[0]
    create = field._to_python(client['create'])

    #--- Список файлов ---
    comfiles = GetComFiles(client_id)

    c = RequestContext(request,{'form':form,'fform':fform,'client':client,'creator':creator,'create':create,'comfiles':comfiles,'ok':com['ok']})
    c.update(csrf(request))
    return render_to_response("client/commercial.html",c)




### Реализация ----
def	Real(request):


    try:
	if CheckAccess(request,'24') != 'OK':
	    return render_to_response("client/notaccess/clientlist.html")
    except:
	return HttpResponseRedirect('/')


    try:
	client_id = request.session['client_id']
    except:
	return HttpResponseRedirect('/clientlist')

    field = DateTimeField()

    client = GetClient(client_id)
    creator = client['creator_name'].split()[1]+' '+client['creator_name'].split()[0]
    create = field._to_python(client['create'])
    

    tech = pickle.loads(client['technical_data'])
    if tech['use'] == u'Стройка':
	return HttpResponseRedirect('/realbuild')
    elif tech['use'] == u'Конфигурация ЦКС':
	return HttpResponseRedirect('/realconfig')
    elif tech['use'] == u'Прокладка UTP/ШПД':
	return HttpResponseRedirect('/realutp')

    c = RequestContext(request,{'client':client,'creator':creator,'create':create})
    c.update(csrf(request))
    return render_to_response("client/real.html",c)






### ---
def	StatusList(request):

    try:
	if CheckAccess(request,'24') != 'OK':
	    return render_to_response("client/notaccess/clientlist.html")
    except:
	return HttpResponseRedirect('/')

    try:
	client_id = request.session['client_id']
    except:
	return HttpResponseRedirect('/clientlist')

    field = DateTimeField()

    client = GetClient(client_id)
    creator = client['creator_name'].split()[1]+' '+client['creator_name'].split()[0]
    create = field._to_python(client['create'])



    data = GetStatusHistory(client_id)


    c = RequestContext(request,{'data':data,'client':client,'creator':creator,'create':create})
    c.update(csrf(request))
    return render_to_response("client/statuslist.html",c)






def	EmailList(request):

    try:
	if CheckAccess(request,'24') != 'OK':
	    return render_to_response("client/notaccess/clientlist.html")
    except:
	return HttpResponseRedirect('/')


    try:
	client_id = request.session['client_id']
    except:
	return HttpResponseRedirect('/clientlist')

    field = DateTimeField()

    client = GetClient(client_id)
    creator = client['creator_name'].split()[1]+' '+client['creator_name'].split()[0]
    create = field._to_python(client['create'])


    data = GetEmailHistory(client_id)



    c = RequestContext(request,{'data':data,'client':client,'creator':creator,'create':create})
    c.update(csrf(request))
    return render_to_response("client/emaillist.html",c)


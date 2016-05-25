#coding:utf-8
from django.shortcuts import render

import	os.path
import	base64

from	operator	import	itemgetter

from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField, BooleanField

from	scatalog.lib.userdata	import	GetUserKod,CheckAccess
from	forms		import	ContractForm,SearchForm,OrderForm,Report1Form
from	scatalog.lib.costcontract	import	NewContract,ListContract,GetContract,EditContract,GetFileData,AddOrder,GetFileOrderData,GetOrderData,EditOrder as EOrder,DelOrder
from	scatalog.lib.costcontract_report	import	Report1,Data2Excel


import	pickle


def	List(request):

    try:
	if CheckAccess(request,'26') != 'OK':
	    return render_to_response("costcontract/notaccess/list.html")
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


    data = ListContract(search)

    paginator = Paginator(data,50)
    try:
	data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
	data_page = paginator.page(paginator.num_pages)

    form = SearchForm(None)
    form.fields['search'].initial = search


    c = RequestContext(request,{'form':form,'data':data_page})
    c.update(csrf(request))
    return render_to_response("costcontract/list.html",c)





def	New(request):

    try:
	if CheckAccess(request,'26') != 'OK':
	    return render_to_response("costcontract/notaccess/list.html")
    except:
	return HttpResponseRedirect('/')


    if request.method == 'POST':
	form = ContractForm(request.POST)
	if form.is_valid():
	    contragent = form.cleaned_data['contragent']
	    tema = form.cleaned_data['tema']
	    block = form.cleaned_data['block']
	    contract = form.cleaned_data['contract']
	    try:
		file_size = request.FILES['file_load'].size
		if file_size <= 104857600:
		    file_name = request.FILES['file_load'].name
		    file_data = request.FILES['file_load'].read()
		    file_name = file_name.split('\\')[-1]
		    (path,ext) = os.path.splitext(file_name)
		    file_name = file_name.replace(' ','_')
		    file_base64 = base64.b64encode(file_data)
		else:
		    file_name = ''
	    except:
		file_name = ''
		file_base64 = ''
		ext = ''

	    NewContract(request,contragent,tema,block,contract,file_name,file_base64,ext)

	    return HttpResponseRedirect('/costcontract')

    form = ContractForm(None)

    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("costcontract/newcontract.html",c)





### --- Основной интерфейс ---
def	Edit(request):

    try:
	if CheckAccess(request,'26') != 'OK':
	    return render_to_response("costcontract/notaccess/list.html")
    except:
	return HttpResponseRedirect('/')


    if request.method == 'GET':
	try:
	    contract_id = request.GET['contract_id']
	    request.session['contract_id'] = contract_id 
	except:
	    pass

    try:
	contract_id = request.session['contract_id']
    except:
	return HttpResponseRedirect('/costcontract')


    if request.method == 'POST':
	form = ContractForm(request.POST)
	if form.is_valid():
	    contragent = form.cleaned_data['contragent']
	    tema = form.cleaned_data['tema']
	    block = form.cleaned_data['block']
	    contract = form.cleaned_data['contract']
	    try:
		file_size = request.FILES['file_load'].size
		if file_size <= 104857600:
		    file_name = request.FILES['file_load'].name
		    file_data = request.FILES['file_load'].read()
		    file_name = file_name.split('\\')[-1]
		    (path,ext) = os.path.splitext(file_name)
		    file_name = file_name.replace(' ','_')
		    file_base64 = base64.b64encode(file_data)
		else:
		    file_name = ''
	    except:
		file_name = ''
		file_base64 = ''
		ext = ''

	    EditContract(contract_id,contragent,tema,block,contract,file_name,file_base64,ext)


	
    con = GetContract(contract_id)

    form = ContractForm(None)
    form.fields['tema'].initial = con['tema']
    form.fields['block'].initial = con['block']
    form.fields['contragent'].initial = con['contragent']
    form.fields['contract'].initial = con['contract']

    file_link = pickle.loads(con['file_data'])

    c = RequestContext(request,{'form':form,'con':con,'file_link':file_link})
    c.update(csrf(request))
    return render_to_response("costcontract/editcontract.html",c)




### --- Файл договора (отдаем) ---
def	File(request):

    try:
	contract_id = request.session['contract_id']
    except:
	return HttpResponseRedirect('/costcontract')

    ### --- Отображение ---
    if request.method == 'GET':

	try:
	    file_id = request.GET['file_id']
	    f = GetFileData(contract_id,file_id)
	    
	    response = HttpResponse(content_type='application/%s' % f['ext'][-1:])
	    attach = u'attachment; filename=\"%s\"' % (f['filename'])
	    response['Content-Disposition'] = attach.encode('utf-8')
	    response.write(base64.b64decode(f['data']))
	    return response

	except:
	    pass

    return HttpResponseRedirect('/costcontract')






### --- Список заказов ---
def	Order(request):

    try:
	if CheckAccess(request,'26') != 'OK':
	    return render_to_response("costcontract/notaccess/list.html")
    except:
	return HttpResponseRedirect('/')

    try:
	contract_id = request.session['contract_id']
    except:
	return HttpResponseRedirect('/costcontract')


    ### --- Отображение ---
    if request.method == 'GET':

	try:
	    delete_id = request.GET['delete_id']
	    DelOrder(contract_id,delete_id)
	except:
	    pass


	try:
	    order_id = request.GET['order_id']
	    f = GetFileOrderData(contract_id,order_id)
	    
	    response = HttpResponse(content_type='application/%s' % f['ext'][-1:])
	    attach = u'attachment; filename=\"%s\"' % (f['filename'])
	    response['Content-Disposition'] = attach.encode('utf-8')
	    response.write(base64.b64decode(f['data']))
	    return response

	except:
	    pass


	
    con = GetContract(contract_id)

    order_data = pickle.loads(con['order_data'])
    data = sorted(order_data,key=lambda x: x['status'])

    file_link = pickle.loads(con['file_data'])

    c = RequestContext(request,{'con':con,'file_link':file_link,'data':data})
    c.update(csrf(request))
    return render_to_response("costcontract/order.html",c)






### --- Новый заказ ---
def	NewOrder(request):

    try:
	if CheckAccess(request,'26') != 'OK':
	    return render_to_response("costcontract/notaccess/list.html")
    except:
	return HttpResponseRedirect('/')

    try:
	contract_id = request.session['contract_id']
    except:
	return HttpResponseRedirect('/costcontract')


    if request.method == 'POST':
	form = OrderForm(request.POST)
	if form.is_valid():
	    order = form.cleaned_data['order']
	    cost = form.cleaned_data['cost']
	    start_date = form.cleaned_data['start_date']
	    end_date = form.cleaned_data['end_date']
	    clientorder = form.cleaned_data['clientorder']
	    status = form.cleaned_data['status']
	    try:
		file_size = request.FILES['file_load'].size
		if file_size <= 104857600:
		    file_name = request.FILES['file_load'].name
		    file_data = request.FILES['file_load'].read()
		    file_name = file_name.split('\\')[-1]
		    (path,ext) = os.path.splitext(file_name)
		    file_name = file_name.replace(' ','_')
		    file_base64 = base64.b64encode(file_data)
		else:
		    file_name = ''
	    except:
		file_name = ''
		file_base64 = ''
		ext = ''

	    AddOrder(request,contract_id,order,cost,start_date,end_date,clientorder,status,file_name,file_base64,ext)
	    return HttpResponseRedirect('/costcontractorder')


	
    con = GetContract(contract_id)

    form = OrderForm(None)

    file_link = pickle.loads(con['file_data'])
    

    c = RequestContext(request,{'form':form,'con':con,'file_link':file_link,'legend':'Создание заказа'})
    c.update(csrf(request))
    return render_to_response("costcontract/editorder.html",c)





### --- Изменение заказа ---
def	EditOrder(request):

    try:
	if CheckAccess(request,'26') != 'OK':
	    return render_to_response("costcontract/notaccess/list.html")
    except:
	return HttpResponseRedirect('/')

    try:
	contract_id = request.session['contract_id']
    except:
	return HttpResponseRedirect('/costcontract')


    if request.method == 'GET':
	try:
	    order_id = request.GET['order_id']
	    request.session['order_id'] = order_id 
	except:
	    pass

    try:
	order_id = request.session['order_id']
    except:
	return HttpResponseRedirect('/costcontractorder')



    if request.method == 'POST':
	form = OrderForm(request.POST)
	if form.is_valid():
	    order = form.cleaned_data['order']
	    cost = form.cleaned_data['cost']
	    start_date = form.cleaned_data['start_date']
	    end_date = form.cleaned_data['end_date']
	    clientorder = form.cleaned_data['clientorder']
	    status = form.cleaned_data['status']
	    try:
		file_size = request.FILES['file_load'].size
		if file_size <= 104857600:
		    file_name = request.FILES['file_load'].name
		    file_data = request.FILES['file_load'].read()
		    file_name = file_name.split('\\')[-1]
		    (path,ext) = os.path.splitext(file_name)
		    file_name = file_name.replace(' ','_')
		    file_base64 = base64.b64encode(file_data)
		else:
		    file_name = ''
	    except:
		file_name = ''
		file_base64 = ''
		ext = ''

	    EOrder(contract_id,order_id,order,cost,start_date,end_date,clientorder,status,file_name,file_base64,ext)
	    return HttpResponseRedirect('/costcontractorder')


	
    con = GetContract(contract_id)

    o = GetOrderData(contract_id,order_id)

    form = OrderForm(None)
    form.fields['order'].initial = o['order']
    form.fields['cost'].initial = o['cost']
    form.fields['start_date'].initial = o['start_date']
    form.fields['end_date'].initial = o['end_date']
    form.fields['clientorder'].initial = o['clientorder']
    form.fields['status'].initial = o['status']

    file_link = pickle.loads(con['file_data'])

    c = RequestContext(request,{'form':form,'con':con,'file_link':file_link,'legend':'Изменение заказа'})
    c.update(csrf(request))
    return render_to_response("costcontract/editorder.html",c)




### --- Отчеты ---
def	Report(request):

    try:
	if CheckAccess(request,'26') != 'OK':
	    return render_to_response("costcontract/notaccess/list.html")
    except:
	return HttpResponseRedirect('/')

    result1 = ''
    tema = ''
    contragent = ''

    if request.method == 'GET':
	try:
	    excel = request.GET['excel']

	    response = HttpResponse(content_type='application/ms-excel')
	    attach = u'attachment; filename=\"report.xls\"'
	    response['Content-Disposition'] = attach.encode('utf-8')

	    return Data2Excel(response)

	except:
	    pass


    if request.method == 'POST':
	form1 = Report1Form(request.POST)
	if form1.is_valid():
	    tema = form1.cleaned_data['tema']
	    contragent = form1.cleaned_data['contragent']
	    result1 = '%s' % Report1(tema,contragent)

    form1 = Report1Form(None)


    c = RequestContext(request,{'form1':form1,'result1':result1,'tema':tema,'contragent':contragent})
    c.update(csrf(request))
    return render_to_response("costcontract/report.html",c)



#coding:utf-8
from django.shortcuts import render

import	os.path
import	base64

from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	scatalog.lib.userdata	import	GetUserKod,CheckAccess
from	scatalog.lib.contract	import	NewContract,ListContract,GetContractData,DelContract
from	forms			import	SearchForm,LoadContract





def	ContractList(request):

    try:
	if CheckAccess(request,'21') != 'OK':
	    return render_to_response("contract/notaccess/contract.html")
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

    if request.method == 'GET':

	try:
	    contract_id = request.GET['contract_id']
	    c = GetContractData(contract_id)

	    response = HttpResponse(content_type='application/%s' % c['ext'][-1:])
	    attach = u'attachment; filename=\"%s\"' % (c['filename'])
	    response['Content-Disposition'] = attach.encode('utf-8')
	    response.write(base64.b64decode(c['data_id']))
	    return response

	except:
	    pass

	try:
	    delete_contract = request.GET['delete_contract']
	    if CheckAccess(request,'22') != 'OK':
		DelContract(delete_contract)
	except:
	    pass
	    

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

    c = RequestContext(request,{'data':data_page,'form':form})
    c.update(csrf(request))
    return render_to_response("contract/contract.html",c)






### --- Загрузка нового договора ---
def	ContractNew(request):


    try:
	if CheckAccess(request,'22') != 'OK':
	    return render_to_response("contract/notaccess/contract.html")
    except:
	return HttpResponseRedirect('/')



    if request.method == 'POST':
	form = LoadContract(request.POST)
	if form.is_valid():
	    try:
		comment = request.POST['comment']
		contragent = request.POST['contragent']
		file_size = request.FILES['file_load'].size
		if file_size <= 104857600:
		    file_name = request.FILES['file_load'].name
		    file_data = request.FILES['file_load'].read()
		    file_name = file_name.split('\\')[-1]
		    (path,ext) = os.path.splitext(file_name)
		    file_name = file_name.replace(' ','_')
		    file_base64 = base64.b64encode(file_data)
		    NewContract(request,contragent,comment,file_name,file_base64,ext)
		    return HttpResponseRedirect('/contract')
	    except:
		pass
    
    form = LoadContract(None)

    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("contract/contractnew.html",c)


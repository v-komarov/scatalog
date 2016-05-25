#coding:utf-8
from django.shortcuts import render


from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	scatalog.lib.userdata	import	GetUserKod,CheckAccess
from	forms			import	SchemeForm,StepForm,GetActionName,AttrForm
from	scatalog.lib.jsondata	import	JsonUser
from	scatalog.lib.scheme	import	CreateScheme,GetSchemeList,GetSchemeData,SaveScheme,AddAttr,AttrList,DelAttr


import	pickle


#-- Проверка - существует ли уже такой шаг ---
def	CheckStep(data,step):
    for item in data['stepdata']:
	if item['step_number'] == step:
	    return False
    return True 


## --- Удаление шага ---
def	DeleteStep(data,step):
    stepdata = data['stepdata']
    for item in stepdata:
	if item['step_number'] == int(step):
	    stepdata.remove(item)
	    data['stepdata'] = stepdata
    return data 






def	SchemeList(request):

    try:
	if CheckAccess(request,'12') != 'OK':
	    return render_to_response("scheme/notaccess/scheme.html")
    except:
	return HttpResponseRedirect('/')



    ### --- Получение номера страницы ---
    try:
	page = int(request.GET.get('page',1))
	request.session['page'] = page
    except:
	pass
	
    try:
	page = int(request.session['page'])
    except:
	page = 1


    data = GetSchemeList()


    paginator = Paginator(data,50)
    try:
	data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
	data_page = paginator.page(paginator.num_pages)


    c = RequestContext(request,{'data':data_page})
    c.update(csrf(request))
    return render_to_response("scheme/schemelist.html",c)






def	SchemeNew(request):


    try:
	if CheckAccess(request,'12') != 'OK':
	    return render_to_response("scheme/notaccess/scheme.html")
    except:
	return HttpResponseRedirect('/')


    if request.method == 'POST':
	
	form = SchemeForm(request.POST)
	if form.is_valid():
	    name = form.cleaned_data['name']
	    result = CreateScheme(request,name)
	    if result:
		return HttpResponseRedirect('/schemeedit/?edit_id=%s' % result)
    

    form = SchemeForm(None)
    stepform = StepForm(None)

    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("scheme/schemenew.html",c)







def	SchemeEdit(request):

    try:
	if CheckAccess(request,'12') != 'OK':
	    return render_to_response("scheme/notaccess/scheme.html")
    except:
	return HttpResponseRedirect('/')
    #del request.session['schemed']

    ### --- Редактирование схемы ---
    try:
	scheme_id = request.GET['edit_id']
	data = GetSchemeData(scheme_id)
	data['scheme_id'] = scheme_id
	request.session['schemed'] = pickle.dumps(data)
	return HttpResponseRedirect('/schemeedit')
    except:
	scheme = request.session['schemed']
	data = pickle.loads(scheme)

    steps = data['stepdata']

    if request.method == 'GET':
	try:
	    delete_step = request.GET['delete_step']
	    data = DeleteStep(data,delete_step)
	    request.session['schemed'] = pickle.dumps(data)
	except:
	    pass


    ### --- Сохранение схемы ---
	try:
	    edit = request.GET['edit']
	    scheme = request.session['schemed']
	    data = pickle.loads(scheme)
	    if SaveScheme(data) == 'OK':
		return HttpResponseRedirect('/scheme')
	except:
	    pass


    if request.method == 'POST':
	
	form = SchemeForm(request.POST)
	if form.is_valid():
	    name = form.cleaned_data['name']
	    data = pickle.loads(request.session['schemed'])
	    data['name'] = name
	    request.session['schemed'] = pickle.dumps(data)


	stepform = StepForm(request.POST)
	if stepform.is_valid():
	    step_number = stepform.cleaned_data['step_number']
	    step_name = stepform.cleaned_data['step_name']
	    user = stepform.cleaned_data['user']
	    action = stepform.cleaned_data['action']
	    step_yes = stepform.cleaned_data['step_yes']
	    step_no = stepform.cleaned_data['step_no']
	    function = stepform.cleaned_data['function']
	    data = pickle.loads(request.session['schemed'])
	    if CheckStep(data,step_number):
	
	
		j = JsonUser(user)
		steps = data['stepdata']

		steps.append({'step_number':step_number,
				'step_name':step_name,
				'user_id':j.j['user_id'],
				'user_name':j.j['name2']+' '+j.j['name1'],
				'user_email':j.j['email'],
				'user_phone':j.j['phone_office'],
				'action_kod':action,
				'action_name':GetActionName(action),
				'step_yes':step_yes,
				'step_no':step_no,
				'function':function
				})
		data['stepdata'] = steps
		steps = sorted(steps)
		request.session['schemed'] = pickle.dumps(data)


    form = SchemeForm(None)
    stepform = StepForm(None)
    form.fields['name'].initial = data['name']

    c = RequestContext(request,{'form':form,'stepform':stepform,'steps':steps})
    c.update(csrf(request))
    return render_to_response("scheme/schemeedit.html",c)






### --- Атрибуты по схеме ---
def	SchemeAttrs(request):

    try:
	if CheckAccess(request,'12') != 'OK':
	    return render_to_response("scheme/notaccess/scheme.html")
    except:
	return HttpResponseRedirect('/')


    ### --- Дополнительные атрибуты ---
    try:
	scheme_id = request.GET['scheme_id']
	request.session['scheme_id'] = scheme_id
    except:
	scheme_id = request.session['scheme_id']

    scheme = GetSchemeData(scheme_id)

    if request.method == 'GET':
	try:
	    attr = request.GET['delete_attr']
	    DelAttr(scheme_id,attr)
	except:
	    pass


    if request.method == 'POST':
	
	form = SchemeForm(request.POST)
	if form.is_valid():
	    name = form.cleaned_data['name']
	    AddAttr(scheme_id,name)

    form = AttrForm(None)

    data = AttrList(scheme_id)

    c = RequestContext(request,{'name':scheme['name'],'form':form,'data':data})
    c.update(csrf(request))
    return render_to_response	("scheme/schemeattrs.html",c)
    

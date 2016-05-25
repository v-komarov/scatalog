#coding:utf-8
from django.shortcuts import render


from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	django.core.paginator	import	Paginator, InvalidPage, EmptyPage

from	scatalog.lib.userdata	import	GetUserKod,CheckAccess
from	scatalog.lib.mtmc	import	NewEq,GetList,GetEq,EditName,AddAttr,GetAttrList,DelAttr,AddData,GetDataList,DelData,AddStatus,GetStatusList,AddM,GetMList,FindKey,AddFile,GetFileList,GetFile,DelFile,TmcUrl
from	forms			import	UserForm,SearchForm,MoveForm,NameForm,AttrForm,DataForm,StatusForm,MForm,LoadFile
from	scatalog.lib.mtmc_print	import	PrintForm

from	cStringIO	import	StringIO

from	couchdb.mapping	import	DateTimeField

import	pickle
import	qrcode
import	base64
import	os.path


### --- Список ---
def	List(request):

    try:
	if CheckAccess(request,'23') != 'OK':
	    return render_to_response("mtmc/notaccess/mtmc.html")
    except:
	return HttpResponseRedirect('/')




    if request.method == 'POST':
	formuser = UserForm(request.POST)
	if formuser.is_valid():
	    user = formuser.cleaned_data['user']
	    request.session['user_id'] = user

	formsearch = SearchForm(request.POST)
	if formsearch.is_valid():
	    search = formsearch.cleaned_data['search']
	    r = FindKey(search)
	    if len(r) == 1:
		return HttpResponseRedirect('/mtmcedit/?eq_id=%s' % search)

    ### --- Сохранное занчение user_id ---
    try:
	user_id = request.session['user_id']
    except:
	user_id = ''

    try:
	print_ok = request.GET['print']
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="list.pdf"'
	buff = StringIO()
	result = PrintForm(buff,user_id)
	response.write(result.getvalue())
	buff.close()
	return response
    except:
	pass



    formmove = MoveForm(None)
    formsearch = SearchForm(None)
    formuser = UserForm(None)
    formuser.fields['user'].initial = user_id


    data = GetList(user_id)

    if len(data)!=0 and user_id != 'ALL':
	print_ok = True
    else:
	print_ok = False

    c = RequestContext(request,{'data':data,'formuser':formuser,'formsearch':formsearch,'formmove':formmove,'print_ok':print_ok})
    c.update(csrf(request))
    return render_to_response("mtmc/list.html",c)






### --- Новый объект ---
def	New(request):

    try:
	if CheckAccess(request,'23') != 'OK':
	    return render_to_response("mtmc/notaccess/mtmc.html")
    except:
	return HttpResponseRedirect('/')


    if request.method == 'POST':
	form = NameForm(request.POST)
	if form.is_valid():
	    name = form.cleaned_data['name']
	    result = NewEq(request,name)
	    if result:
		return HttpResponseRedirect('/mtmcedit/?eq_id=%s' % result)


    form = NameForm(None)



    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("mtmc/new.html",c)






### --- Объект ---
def	Edit(request):

    try:
	if CheckAccess(request,'23') != 'OK':
	    return render_to_response("mtmc/notaccess/mtmc.html")
    except:
	return HttpResponseRedirect('/')

    try:
	eq_id = request.GET['eq_id']
	request.session['eq_id'] = eq_id
    except:
	pass

    try:
	eq_id = request.session['eq_id']
    except:
	return HttpResponseRedirect('/mtmc')
	

    if request.method == 'POST':
	form = NameForm(request.POST)
	if form.is_valid():
	    name = form.cleaned_data['name']
	    EditName(eq_id,name)

    eq = GetEq(eq_id)

    form = NameForm(None)
    form.fields['name'].initial = eq['name']
    
    field = DateTimeField()
    create = field._to_python(eq['create'])
    author = eq['author_name'].split()[1]+' '+eq['author_name'].split()[0]

    c = RequestContext(request,{'form':form,'eq':eq,'create':create,'author':author,'tmc':TmcUrl(eq)})
    c.update(csrf(request))
    return render_to_response("mtmc/edit.html",c)





### --- Атрибуты ---
def	Attrs(request):

    try:
	if CheckAccess(request,'23') != 'OK':
	    return render_to_response("mtmc/notaccess/mtmc.html")
    except:
	return HttpResponseRedirect('/')


    try:
	eq_id = request.session['eq_id']
    except:
	return HttpResponseRedirect('/mtmc')
	

    try:
	attr_id = request.GET['attr_delete']
	DelAttr(eq_id,attr_id)
    except:
	pass


    if request.method == 'POST':
	form = AttrForm(request.POST)
	if form.is_valid():
	    attr = form.cleaned_data['attr']
	    value = form.cleaned_data['value']
	    AddAttr(eq_id,attr,value,request)

    eq = GetEq(eq_id)

    

    form = AttrForm(None)

    data = GetAttrList(eq_id)
    
    c = RequestContext(request,{'form':form,'eq':eq,'data':data,'tmc':TmcUrl(eq)})
    c.update(csrf(request))
    return render_to_response("mtmc/attrs.html",c)





### --- Компоненты ---
def	Data(request):

    try:
	if CheckAccess(request,'23') != 'OK':
	    return render_to_response("mtmc/notaccess/mtmc.html")
    except:
	return HttpResponseRedirect('/')


    try:
	eq_id = request.session['eq_id']
    except:
	return HttpResponseRedirect('/mtmc')
	

    try:
	data_id = request.GET['data_delete']
	DelData(eq_id,data_id)
    except:
	pass


    if request.method == 'POST':
	form = DataForm(request.POST)
	if form.is_valid():
	    d = form.cleaned_data['d']
	    q = form.cleaned_data['q']
	    AddData(eq_id,d,q,request)

    eq = GetEq(eq_id)

    form = DataForm(None)
    form.fields['q'].initial = 1

    data = GetDataList(eq_id)
    
    c = RequestContext(request,{'form':form,'eq':eq,'data':data,'tmc':TmcUrl(eq)})
    c.update(csrf(request))
    return render_to_response("mtmc/data.html",c)





### --- Статус ---
def	Status(request):

    try:
	if CheckAccess(request,'23') != 'OK':
	    return render_to_response("mtmc/notaccess/mtmc.html")
    except:
	return HttpResponseRedirect('/')


    try:
	eq_id = request.session['eq_id']
    except:
	return HttpResponseRedirect('/mtmc')
	


    if request.method == 'POST':
	form = StatusForm(request.POST)
	if form.is_valid():
	    status = form.cleaned_data['status']
	    comment = form.cleaned_data['comment']
	    AddStatus(eq_id,status,comment,request)

    eq = GetEq(eq_id)

    form = StatusForm(None)

    data = GetStatusList(eq_id)
    
    c = RequestContext(request,{'form':form,'eq':eq,'data':data,'tmc':TmcUrl(eq)})
    c.update(csrf(request))
    return render_to_response("mtmc/status.html",c)





### --- Перемещения ---
def	Move(request):

    try:
	if CheckAccess(request,'23') != 'OK':
	    return render_to_response("mtmc/notaccess/mtmc.html")
    except:
	return HttpResponseRedirect('/')


    try:
	eq_id = request.session['eq_id']
    except:
	return HttpResponseRedirect('/mtmc')
	


    if request.method == 'POST':
	form = MForm(request.POST)
	if form.is_valid():
	    user = form.cleaned_data['user']
	    place = form.cleaned_data['place']
	    AddM(eq_id,user,place,request)

    eq = GetEq(eq_id)

    form = MForm(None)

    data = GetMList(eq_id)
    
    c = RequestContext(request,{'form':form,'eq':eq,'data':data,'tmc':TmcUrl(eq)})
    c.update(csrf(request))
    return render_to_response("mtmc/move.html",c)





### --- Приложения ---
def	Files(request):

    try:
	if CheckAccess(request,'23') != 'OK':
	    return render_to_response("mtmc/notaccess/mtmc.html")
    except:
	return HttpResponseRedirect('/')


    try:
	eq_id = request.session['eq_id']
    except:
	return HttpResponseRedirect('/mtmc')
	

    try:
	file_id = request.GET['file_delete']
	DelFile(eq_id,file_id)
    except:
	pass

    try:
	file_id = request.GET['get_file']
	f = GetFile(eq_id,file_id)
	response = HttpResponse(content_type='application/%s' % f['file_ext'][-1:])
	attach = u'attachment; filename=\"%s\"' % (f['file_name'])
	response['Content-Disposition'] = attach.encode('utf-8')
	response.write(base64.b64decode(f['file_data']))
	return response
    except:
	pass


    if request.method == 'POST':
	form = LoadFile(request.POST)
	if form.is_valid():
	    try:
		comment = request.POST['comment']
		file_size = request.FILES['file_load'].size
		if file_size <= 104857600:
		    file_name = request.FILES['file_load'].name
		    file_data = request.FILES['file_load'].read()
		    file_name = file_name.split('\\')[-1]
		    (path,ext) = os.path.splitext(file_name)
		    file_name = file_name.replace(' ','_')
		    file_base64 = base64.b64encode(file_data)
		    AddFile(eq_id,file_name,comment,file_base64,ext,request)
	    except:
		pass


    eq = GetEq(eq_id)

    form = LoadFile(None)

    data = GetFileList(eq_id)
    
    c = RequestContext(request,{'form':form,'eq':eq,'data':data,'tmc':TmcUrl(eq)})
    c.update(csrf(request))
    return render_to_response("mtmc/files.html",c)



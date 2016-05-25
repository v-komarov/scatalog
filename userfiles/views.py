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

from	scatalog.lib.userdata	import	GetUserKod,GetEmail,GetFio,GetPhone
from	forms			import	LoadFile,SendLinkFile,SearchForm,AccessType,AccessUser,EditComment
from	scatalog.lib.userfiles	import	NewFile,ListFile,GetFileData,DelFile,GetEmailList,SetTypeAccess,GetAccessUser,AddUserData,DelUserAccess,ListOtherFile,SaveComment
from	scatalog.lib.userfiles_mail	import	FileLink


def	List(request):

    try:
	user = GetUserKod(request)
    except:
	return HttpResponseRedirect('/')


    ### --- Удаление файла ---
    if request.method == 'GET':
	try:
	    delete_id = request.GET['delete_file']
	    DelFile(delete_id)
	except:
	    pass


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



    try:
	search = request.session['search']
    except:
	search = ''



    if request.method == 'POST':
	
	form = SearchForm(request.POST)
	if form.is_valid():
	    search = form.cleaned_data['search']
	    request.session['search'] = search

    data = ListFile(user,search)


    paginator = Paginator(data,50)
    try:
	data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
	data_page = paginator.page(paginator.num_pages)

    form = SearchForm(None)
    form.fields['search'].initial = search

    c = RequestContext(request,{'data':data_page,'form':form})
    c.update(csrf(request))
    return render_to_response("userfiles/list.html",c)



### --- Новый файл ---
def	New(request):

    try:
	user = GetUserKod(request)
    except:
	return HttpResponseRedirect('/')


    if request.method == 'POST':
	form = LoadFile(request.POST)
	if form.is_valid():
	    try:
		comment = request.POST['comment']
		file_size = request.FILES['file_load'].size
#		if file_size <= 5242880: 5Mb
#		if file_size <= 20971520: 20Mb
		if file_size <= 104857600:
		    file_name = request.FILES['file_load'].name
		    file_data = request.FILES['file_load'].read()
		    file_name = file_name.split('\\')[-1]
		    (path,ext) = os.path.splitext(file_name)
		    file_name = file_name.replace(' ','_')
		    file_base64 = base64.b64encode(file_data)
		    NewFile(GetUserKod(request),GetFio(request),GetPhone(request),GetEmail(request),comment,file_name,file_base64,ext,file_size)
		    return HttpResponseRedirect('/userfiles')
	    except:
		pass
    
    form = LoadFile(None)

    c = RequestContext(request,{'form':form})
    c.update(csrf(request))
    return render_to_response("userfiles/newfile.html",c)




##--- Отдаем файл ---
def	GetFile(request):

    ### --- Отображение ---
    if request.method == 'GET':
	try:
	    file_id = request.GET['file_id']
	    f = GetFileData(file_id)
	    
	    access_user = 'NOT'

	    if f['access'].encode('utf-8') == 'user':
		users = f['users']
		for u in users:
		    if u[0].encode('utf-8') == GetUserKod(request):
			access_user = 'YES'
	    try:
		if f['author'].encode('utf-8') == GetUserKod(request):
		    access_user = 'YES'
	    except:
		pass

	    if f['access'].encode('utf-8') == 'public':
		access_user = 'YES'


	    if access_user == 'YES':
		response = HttpResponse(content_type='application/%s' % f['ext'][-1:])
		attach = u'attachment; filename=\"%s\"' % (f['filename'])
		response['Content-Disposition'] = attach.encode('utf-8')
		response.write(base64.b64decode(f['data_id']))
		return response
	except:
	    return HttpResponseRedirect('/userfiles')




def	SendFile(request):

    try:
	user = GetUserKod(request)
    except:
	return HttpResponseRedirect('/')


    if request.method == 'GET':
	try:
	    file_id = request.GET['file_id']
	    request.session['file_id'] = file_id 
	except:
	    pass

    try:
	file_id = request.session['file_id']
    except:
	return HttpResponseRedirect('/userfiles')


    f_data = GetFileData(file_id)


    if request.method == 'POST':
	
	form = SendLinkFile(request.POST)
	if form.is_valid():
	    comment = form.cleaned_data['comment']
	    user = form.cleaned_data['user']
	    FileLink(user,GetEmail(request),comment,f_data['filename'],file_id)
	    return HttpResponseRedirect('/userfiles')


	
    form = SendLinkFile(None)
    

    c = RequestContext(request,{'form':form,'filename':f_data['filename']})
    c.update(csrf(request))
    return render_to_response("userfiles/sendurl.html",c)





### --- Доступ к файлу ---
def	AccessFile(request):

    try:
	user = GetUserKod(request)
    except:
	return HttpResponseRedirect('/')


    if request.method == 'GET':
	try:
	    file_id = request.GET['file_id']
	    request.session['file_id'] = file_id 
	except:
	    pass

    try:
	file_id = request.session['file_id']
    except:
	return HttpResponseRedirect('/userfiles')

    f = GetFileData(file_id)


    if f['author'].encode("utf-8") != GetUserKod(request):
	return HttpResponseRedirect('/userfiles')
	


    if request.method == 'POST':
	
	form = AccessType(request.POST)
	if form.is_valid():
	    access = form.cleaned_data['access']
	    SetTypeAccess(file_id,access)
	    if access == 'public' or access == 'private':
		return HttpResponseRedirect('/userfiles')

	form2 = AccessUser(request.POST)
	if form2.is_valid():
	    user = form2.cleaned_data['user']
	    AddUserData(user,file_id,request)


    if request.method == 'GET':
	try:
	    deluser_id = request.GET['deluser_id']
	    DelUserAccess(deluser_id,file_id)
	except:
	    pass

    f = GetFileData(file_id)

    
	
    form = AccessType(None)
    access = f['access'].encode('utf-8')
    form.fields['access'].initial = access

    form2 = AccessUser(None)
    form2.fields['user'].initial = ''
    
    fname = f['filename'].encode("utf-8")

    accessuser = GetAccessUser(file_id)

    c = RequestContext(request,{'form':form,'access':access,'fname':fname,'form2':form2,'accessuser':accessuser})
    c.update(csrf(request))
    return render_to_response("userfiles/access.html",c)







def	OtherFiles(request):

    try:
	user = GetUserKod(request)
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



    try:
	search = request.session['search']
    except:
	search = ''



    if request.method == 'POST':
	
	form = SearchForm(request.POST)
	if form.is_valid():
	    search = form.cleaned_data['search']
	    request.session['search'] = search

    data = ListOtherFile(user,search)


    paginator = Paginator(data,50)
    try:
	data_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
	data_page = paginator.page(paginator.num_pages)

    form = SearchForm(None)
    form.fields['search'].initial = search

    c = RequestContext(request,{'data':data_page,'form':form})
    c.update(csrf(request))
    return render_to_response("userfiles/other.html",c)




def	Edit(request):


    try:
	user = GetUserKod(request)
    except:
	return HttpResponseRedirect('/')


    if request.method == 'GET':
	try:
	    file_id = request.GET['file_id']
	    request.session['file_id'] = file_id 
	except:
	    pass

    try:
	file_id = request.session['file_id']
    except:
	return HttpResponseRedirect('/userfiles')

    f = GetFileData(file_id)


    if f['author'].encode("utf-8") != GetUserKod(request):
	return HttpResponseRedirect('/userfiles')
	


    if request.method == 'POST':
	
	form = EditComment(request.POST)
	if form.is_valid():
	    comment = form.cleaned_data['comment']
	    SaveComment(file_id,comment)
	    return HttpResponseRedirect('/userfiles')


    form = EditComment(None)
    form.fields['comment'].initial = f['comment'].encode('utf-8')
    
    fname = f['filename'].encode("utf-8")

    c = RequestContext(request,{'form':form,'fname':fname})
    c.update(csrf(request))
    return render_to_response("userfiles/comment.html",c)

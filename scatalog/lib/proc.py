#coding:utf-8

import	datetime
import	cPickle
import	time

from	operator	import	itemgetter


from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField, BooleanField
from	jsondata	import	UserEmailList,UserList,JsonUser
from	userdata	import	GetEmail,GetPhone,GetFio,GetUserKod


server = Server()


class	Proc(Document):
    proc_num = IntegerField()
    proc_name = TextField()
    scheme_link = TextField()
    next_step = IntegerField(default=0)
    status = TextField()
    info = TextField()
    author = TextField()
    author_name = TextField()
    author_phone = TextField()
    author_email = TextField()
    create = DateTimeField(default=datetime.datetime.now())
    comment_data = TextField(default=cPickle.dumps([]))
    step_data = TextField(default=cPickle.dumps([]))
    email_data = TextField(default=cPickle.dumps([]))
    attr_data = TextField(default=cPickle.dumps([]))




### --- Определение proc_num ---
def	NextProcNum():

    db = server['proc']
    map_fun = '''function(doc) {
	emit(doc._id,doc.proc_num);
    }'''

    data = []

    for row in db.query(map_fun):
	data.append(row.value)

    if len(data) == 0:
	return 1
    else:
	sorted(data)
	return data[-1]+1










### --- Список схем ---
def	GetSchemeList():

    db = server['scheme']
    map_fun = '''function(doc) {
	emit(doc._id,doc.scheme_name);
    }'''

    data = []

    for row in db.query(map_fun):
	data.append([row.key,row.value])

    sorted(data)

    return data









### --- Запись одного процесса ---
def	GetProc(proc_id):

    db = server['proc']
    return db[proc_id]









def	ListFile(author):


    db = server['userfiles']
    map_fun = '''function(doc) {
	if (doc.author == '%s' && doc.access != 'private')
	    emit(doc._id,doc.filename);
    }''' % author

    data = []

    for row in db.query(map_fun):
	    data.append([row.key+'#'+row.value,row.value])

    data = sorted(data,key=itemgetter(1))

    return data





def	ListFileAll():


    db = server['userfiles']
    map_fun = '''function(doc) {
	if (doc.access != 'private')
	    emit(doc._id,doc.filename);
    }'''

    data = []

    for row in db.query(map_fun):
	    data.append([row.key+'#'+row.value,row.value])

    return data






def	AddComment(proc_id,file_id,file_name,comment,request):

    user_kod = GetUserKod(request)
    user_name = GetFio(request).split()

    d = {'id':int(time.time()),
    'create':datetime.datetime.now(),
    'file_id':file_id,
    'file_name':file_name,
    'comment':comment,
    'email':GetEmail(request),
    'author_kod':user_kod,
    'author_name':user_name[1]+' '+user_name[0]}

    db = server['proc']
    proc = db[proc_id]
    data = cPickle.loads(proc['comment_data'].encode('utf-8'))
    data.append(d)
    proc['comment_data'] = cPickle.dumps(data)

    db.save(proc)

    return 'OK'






### --- Список приложений ---
def	GetCommentList(proc_id):

    db = server['proc']
    proc = db[proc_id]
    data = cPickle.loads(proc['comment_data'].encode('utf-8'))
    data.reverse()

    return data




def	DelComment(proc_id,comment_id,request):

    db = server['proc']
    proc = db[proc_id]
    data = cPickle.loads(proc['comment_data'].encode('utf-8'))
    for row in data:
	if row['id'] == int(comment_id) and row['author_kod'] == GetUserKod(request):
	    data.remove(row)
    proc['comment_data'] = cPickle.dumps(data)

    db.save(proc)








### --- Определение следующего шага ---
def	NextStep(proc_id):

    pdb = server['proc']
    p = pdb[proc_id]

    scheme_link = p['scheme_link']
    if scheme_link == "":
	return 0

    ### --- История шагов ---
    stephistory = cPickle.loads(p['step_data'].encode('utf-8'))

    ## --- Набор шагов по схеме ---
    sdb = server['scheme']
    s = sdb[scheme_link]
    stepscheme = cPickle.loads(s['step_data'].encode('utf-8'))

    ### --- Для случая , когда шагов пока не было ---
    if len(stephistory) == 0:
	for i in stepscheme:
	    if i['action_kod'] == u'begin':
		return i['step_number']

    ### --- Последний шаг, который зафиксирован ---
    for step in stephistory:
	if step['scheme_link'] != scheme_link:
	    stephistory.remove(step)

    if len(stephistory) == 0:
	for i in stepscheme:
	    if i['action_kod'] == u'begin':
		return i['step_number']
    else:
	last_step = stephistory[-1]
	last_number = last_step['step_number']
	result = last_step['result']

	if result == u'yes':
	    for i in stepscheme:
		if i['step_number'] == last_number:
		    next_step = i['step_yes']
	else:
	    for i in stepscheme:
		if i['step_number'] == last_number:
		    next_step = i['step_no']

	for j in stepscheme:
	    if j['action_kod'] == u'end' and j['step_number'] == next_step:
		return 1000

	return next_step








### --- Сохранение данных процесса ---
def	SaveProcData(request,proc_id,name,scheme,status,info):

    db = server['proc']
    proc = db[proc_id]

    author = proc['author']

    if GetUserKod(request) == author:

	proc['scheme_link'] = scheme
	proc['proc_name'] = name
	proc['status'] = status
	proc['info'] = info
	db.save(proc)

    ### --- Фиксируем расчетный следующий шаг ---
    next_step = NextStep(proc_id)
    proc = db[proc_id]
    proc['next_step'] = next_step
    if next_step == 1000:
	proc['status'] = 'Завершен'
	db.save(proc)
	return 'OVER'
    db.save(proc)

    return 'OK'





### --- Первоначальное создание процесса ---
def	NewProc(request):

    db = server['proc']

    myproc = Proc(proc_num=NextProcNum(),proc_name='_',scheme_link='',next_step=0,status=u'Подготовка',author=GetUserKod(request),author_name=GetFio(request),author_email=GetEmail(request),author_phone=GetPhone(request))
    doc = myproc.store(db)

    return doc.id




### --- Определение следующего согласующего ---
def	NextPerson(proc_id):

    next_person = {'kod':'','person':'','email':'','phone':'','proc_link':'','step_number':0,'step_name':'','scheme_link':''}

    db = server['proc']
    proc = db[proc_id]

    scheme_link = proc['scheme_link']
    next_step = proc['next_step']

    if next_step == 0 or next_step == 1000:
	return next_person

    dbs = server['scheme']
    scheme = dbs[scheme_link]
    scheme_step = cPickle.loads(scheme['step_data'].encode('utf-8'))

    for item in scheme_step:
	if item['step_number'] == next_step:
	    next_person['kod'] = item['user_id']
	    next_person['person'] = item['user_name']
	    next_person['email'] = item['user_email']
	    next_person['phone'] = item['user_phone']
	    next_person['proc_link'] = proc_id
	    next_person['step_number'] = next_step
	    next_person['step_name'] = item['step_name']
	    next_person['scheme_link'] = scheme_link

    return next_person




### --- Пишем результат согласования ---
def	PointStep(proc_id,yesno,comment,next_person):


    db = server['proc']
    proc = db[proc_id]
    data = cPickle.loads(proc['step_data'].encode('utf-8'))
    step = {
	'create':datetime.datetime.now(),
	'result':yesno.decode('utf-8'),
	'comment':comment.decode('utf-8'),
	'person':next_person['person'],
	'email':next_person['email'],
	'phone':next_person['phone'],
	'step_name':next_person['step_name'],
	'step_number':next_person['step_number'],
	'scheme_link':next_person['scheme_link']
	    }

    data.append(step)
    proc['step_data'] = cPickle.dumps(data)
    db.save(proc)

    proc = db[proc_id]
    next_step = NextStep(proc_id)
    if next_step == 1000:
	proc['status'] = u'Завершен'
    proc['next_step'] = next_step 
    db.save(proc)


    return 'OK'



### --- Список решений согласования  ---
def	ListStepHistory(proc_id):

    db = server['proc']
    proc = db[proc_id]
    data = cPickle.loads(proc['step_data'].encode('utf-8'))
    
    data.reverse()

    return data







### --- Список процессов ---
def	GetProcList():

    scheme_db = server['scheme']

    db = server['proc']
    map_fun = '''function(doc) {
	emit(doc.proc_num,[doc._id,doc.proc_name,doc.status,doc.create,doc.scheme_link,doc.next_step,doc.author_name]);
    }'''

    data = []

    field = DateTimeField()

    for row in db.query(map_fun):
	if row.value[4] == '':
	    scheme = ''
	    step = ''
	    user = {'person':'','phone':''}
	else:
	    doc = scheme_db[row.value[4]]
	    scheme = doc['scheme_name']
	    user = NextPerson(row.value[0])

	if row.value[5] == 0:
	    next_step = 'Start'
	elif row.value[5] == 1000:
	    next_step = 'End'
	else:
	    next_step = row.value[5]
	author = row.value[6].split()[1]+' '+row.value[6].split()[0]
	data.append([row.key,row.value[0],row.value[1],row.value[2],field._to_python(row.value[3]),scheme,next_step,user['person']+' ('+user['phone']+')',author])

    data.reverse()

    return data



### --- Получение возможных атрибутов для схемы ---
def	GetAttrs(proc_id):

    proc_db = server['proc']
    proc = proc_db[proc_id]
    scheme_link = proc['scheme_link']
    scheme_db = server['scheme']
    scheme = scheme_db[scheme_link]
    attrs_list = scheme['attrs_list']
    result = [['',''],]
    for i in attrs_list:
	result.append([i,i])

    return result



### --- Получение всех возможных атрибутов для схемы ---
def	GetAttrsAll():

    db = server['scheme']
    map_fun = '''function(doc) {
	emit(doc.scheme_id,doc.attrs_list);
    }'''

    data = []

    for row in db.query(map_fun):
	attr = row.value
	for i in attr:
	    data.append([i,i])

    return data




def	AddAttr(proc_id,attr,value,request):

    user_kod = GetUserKod(request)
    user_name = GetFio(request).split()

    d = {'id':int(time.time()),
    'create':datetime.datetime.now(),
    'attr':attr,
    'value':value,
    'email':GetEmail(request),
    'author_kod':user_kod,
    'author_name':user_name[1]+' '+user_name[0]}

    db = server['proc']
    proc = db[proc_id]
    data = cPickle.loads(proc['attr_data'].encode('utf-8'))
    data.append(d)
    proc['attr_data'] = cPickle.dumps(data)

    db.save(proc)

    return 'OK'





### --- Список дополнительных атрибутов ---
def	GetAttrList(proc_id):

    db = server['proc']
    proc = db[proc_id]
    data = cPickle.loads(proc['attr_data'].encode('utf-8'))
    data.reverse()

    return data




def	DelAttr(proc_id,attr_id):

    db = server['proc']
    proc = db[proc_id]
    data = cPickle.loads(proc['attr_data'].encode('utf-8'))
    for row in data:
	if row['id'] == int(attr_id):
	    data.remove(row)
    proc['attr_data'] = cPickle.dumps(data)

    db.save(proc)


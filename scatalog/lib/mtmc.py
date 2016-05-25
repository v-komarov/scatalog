#coding:utf-8

import	datetime
import	pickle
import	time
import	qrcode

from	operator	import	itemgetter


from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField, BooleanField
from	jsondata	import	UserEmailList,UserList,JsonUser
from	userdata	import	GetEmail,GetPhone,GetFio,GetUserKod


server = Server()


class	Eq(Document):
    name = TextField()
    status = TextField(default='')
    user_kod = TextField(default='')
    user_name = TextField(default='')
    user_phone = TextField(default='')
    user_email = TextField(default='')
    area = TextField(default='')
    attrs_data = TextField(default=pickle.dumps([]))
    move_data = TextField(default=pickle.dumps([]))
    status_data = TextField(default=pickle.dumps([]))
    component_data = TextField(default=pickle.dumps([]))
    file_data = TextField(default=pickle.dumps([]))
    create = DateTimeField(default=datetime.datetime.now())
    author_kod = TextField()
    author_name = TextField()
    author_phone = TextField()
    author_email = TextField()


class	FileData(Document):
    data = TextField()



### --- Поиск заявки ТМЦ ---
def	TmcUrl(eq):
    attrs_data = pickle.loads(eq['attrs_data'])
    for item in attrs_data:
	if item['attr'].replace(' ','').lower() == u'заявкатмц':
	    return item['value']

    return False




### --- Список для выбора пользователя ---
def	GetUserList():

    e = UserList()
    
    data = []

    for key in e.j.keys():
	data.append([key,e.j[key][2]+' '+e.j[key][1]])

    data = sorted(data,key=itemgetter(1))

    return data




### --- Создание нового объекта ---
def	NewEq(request,name):

    if name == '':
	name = '__________'

    db = server['mtmc']

    new = Eq(

    name = name,

    author_kod=GetUserKod(request),
    author_name=GetFio(request),
    author_phone=GetPhone(request),
    author_email=GetEmail(request))
    doc = new.store(db)

    ### --- Создание qrcode ---
    f = open('scatalog/static/img/qrcode/%s.png' % doc.id,'w')
    img = qrcode.make('http://10.6.1.10:8000/mtmcedit/?eq_id=%s' % doc.id)
    img.save(f,'PNG')
    f.close()

    return doc.id




### --- Список объектов ---
def	GetList(user):

    db = server['mtmc']

    if user == 'ALL':
	map_fun = '''function(doc) {
	    emit(doc._id,[doc.name,doc.status,doc.area,doc.user_name]);
	}'''
    else:
	map_fun = '''function(doc) {
	    if(doc.user_kod == '%s')
	    emit(doc._id,[doc.name,doc.status,doc.area,doc.user_name]);
	}''' % user

    data = []

    for row in db.query(map_fun):
	data.append([
	    row.key,
	    row.value[0],
	    row.value[1],
	    row.value[2],
	    row.value[3]
	    ])

    data = sorted(data,key=itemgetter(1))

    return data



### --- Данные по объекту ---
def	GetEq(eq_id):

    db = server['mtmc']
    eq = db[eq_id]

    return eq



### --- Сохранение названия ---
def	EditName(eq_id,name):

    db = server['mtmc']
    eq = db[eq_id]
    eq['name'] = name

    db.save(eq)

    return 'OK'



### --- Добавление атрибутов ---
def	AddAttr(eq_id,attr,value,request):

    user_kod = GetUserKod(request)
    user_name = GetFio(request).split()

    d = {'id':int(time.time()),
    'create':datetime.datetime.now(),
    'attr':attr,
    'value':value,
    'email':GetEmail(request),
    'author_kod':user_kod,
    'author_name':user_name[1]+' '+user_name[0]}

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['attrs_data'].encode('utf-8'))
    data.append(d)
    eq['attrs_data'] = pickle.dumps(data)

    db.save(eq)

    return 'OK'





### --- Список дополнительных атрибутов ---
def	GetAttrList(eq_id):

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['attrs_data'].encode('utf-8'))
    data = sorted(data,key=itemgetter('attr'))

    return data




def	DelAttr(eq_id,attr_id):

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['attrs_data'].encode('utf-8'))
    for row in data:
	if row['id'] == int(attr_id):
	    data.remove(row)
    eq['attrs_data'] = pickle.dumps(data)

    db.save(eq)





### --- Добавление компонента ---
def	AddData(eq_id,d,q,request):

    user_kod = GetUserKod(request)
    user_name = GetFio(request).split()

    d = {'id':int(time.time()),
    'create':datetime.datetime.now(),
    'd':d,
    'q':q,
    'email':GetEmail(request),
    'author_kod':user_kod,
    'author_name':user_name[1]+' '+user_name[0]}

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['component_data'].encode('utf-8'))
    data.append(d)
    eq['component_data'] = pickle.dumps(data)

    db.save(eq)

    return 'OK'





### --- Список компонентов ---
def	GetDataList(eq_id):

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['component_data'].encode('utf-8'))
    data = sorted(data,key=itemgetter('d'))

    return data




def	DelData(eq_id,d_id):

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['component_data'].encode('utf-8'))
    for row in data:
	if row['id'] == int(d_id):
	    data.remove(row)
    eq['component_data'] = pickle.dumps(data)

    db.save(eq)




### --- Установка статуса ---
def	AddStatus(eq_id,status,comment,request):

    user_kod = GetUserKod(request)
    user_name = GetFio(request).split()

    s = {'id':int(time.time()),
    'create':datetime.datetime.now(),
    'status':status,
    'comment':comment,
    'email':GetEmail(request),
    'author_kod':user_kod,
    'author_name':user_name[1]+' '+user_name[0]}

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['status_data'].encode('utf-8'))
    data.append(s)
    eq['status_data'] = pickle.dumps(data)
    eq['status'] = status

    db.save(eq)

    return 'OK'





### --- История статусов ---
def	GetStatusList(eq_id):

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['status_data'].encode('utf-8'))
    data = sorted(data,key=itemgetter('create'))
    data.reverse()

    return data





### --- Перемещение ---
def	AddM(eq_id,user,area,request):

    user_kod = GetUserKod(request)
    user_name = GetFio(request).split()


    j = JsonUser(user)
    name = j.j['name2']+' '+j.j['name1']
    email = j.j['email']
    phone = j.j['phone_office']

    m = {'id':int(time.time()),
    'create':datetime.datetime.now(),
    'user_kod':user,
    'user_name':name,
    'user_phone':phone,
    'user_email':email,
    'area':area,
    'email':GetEmail(request),
    'author_kod':user_kod,
    'author_name':user_name[1]+' '+user_name[0]}

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['move_data'].encode('utf-8'))
    data.append(m)
    eq['move_data'] = pickle.dumps(data)
    eq['area'] = area
    eq['user_kod'] = user
    eq['user_name'] = name
    eq['user_phone'] = phone
    eq['user_email'] = email

    db.save(eq)

    return 'OK'





### --- История перемещений ---
def	GetMList(eq_id):

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['move_data'].encode('utf-8'))
    data = sorted(data,key=itemgetter('create'))
    data.reverse()

    return data



### --- Поиск объекта по ключу ---
def	FindKey(key):

    db = server['mtmc']

    map_fun = '''function(doc) {
	if(doc._id == '%s')
	emit(doc._id,doc._id);
    }''' % key

    results = db.query(map_fun)

    return results




### --- Добавить файл ---
def	AddFile(eq_id,file_name,comment,file_base64,ext,request):

    dbf = server['mtmc_filedata']
    new = FileData(data=file_base64)
    doc = new.store(dbf)
    file_id = doc.id

    user_kod = GetUserKod(request)
    user_name = GetFio(request).split()

    f = {'id':int(time.time()),
    'create':datetime.datetime.now(),
    'file_id':file_id,
    'file_name':file_name,
    'file_ext':ext,
    'comment':comment,
    'email':GetEmail(request),
    'author_kod':user_kod,
    'author_name':user_name[1]+' '+user_name[0]}

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['file_data'].encode('utf-8'))
    data.append(f)
    eq['file_data'] = pickle.dumps(data)

    db.save(eq)

    return 'OK'




### --- Список файлов ---
def	GetFileList(eq_id):

    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['file_data'].encode('utf-8'))
    data = sorted(data,key=itemgetter('file_name'))

    return data


### --- Отдаем файл ---
def	GetFile(eq_id,file_id):
    
    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['file_data'].encode('utf-8'))
    
    result = {}

    for row in data:
	if row['id'] == int(file_id):
	    result['file_ext'] = row['file_ext']
	    result['file_name'] = row['file_name']
	    file_link = row['file_id']
	    db = server['mtmc_filedata']
	    file_data = db[file_link]
	    result['file_data'] = file_data['data']

	    return result



### --- Удаляем файл ---
def	DelFile(eq_id,file_id):
    
    db = server['mtmc']
    eq = db[eq_id]
    data = pickle.loads(eq['file_data'].encode('utf-8'))
    
    for row in data:
	if row['id'] == int(file_id):
	    file_link = row['file_id']
	    dbf = server['mtmc_filedata']
	    file_data = dbf[file_link]
	    dbf.delete(file_data)
	    data.remove(row)

    eq['file_data'] = pickle.dumps(data)
    db.save(eq)


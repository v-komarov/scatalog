#coding:utf-8

import	datetime
import	pickle
import	time

from	operator	import	itemgetter


from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField, BooleanField
from	jsondata	import	UserEmailList,UserList,JsonUser
from	userdata	import	GetEmail,GetPhone,GetFio,GetUserKod

from	common		import	Compare


server = Server()


class	Client(Document):

    name = TextField()
    address = TextField()
    inn = TextField()
    product = TextField(default=0)
    point = TextField()
    manager_name = TextField()
    manager_kod = TextField()
    manager_phone = TextField()

    service = TextField()
    speed = TextField()
    interface = TextField()
    option = TextField()

    client = TextField()
    email = TextField()
    phone = TextField()

    status = TextField(default=u'Заказ')


    creator_kod = TextField()
    creator_name = TextField()
    creator_email = TextField()
    creator_phone = TextField()
    create = DateTimeField(default=datetime.datetime.now())

    in_work = TextField(default="")
    in_real = TextField(default="")
    priority = TextField(default="")

    file_data = TextField(default=pickle.dumps([]))

    technical_data = TextField(default=pickle.dumps({'use':'','onepay':0.00,'monthpay':0.00,'option':'','jobokp':'','nemis':0,'comment':'','file_data':[]}))
    commercial_data = TextField(default=pickle.dumps({'kp':datetime.date.today(),'onepay':0.00,'monthpay':0.00,'result':'','manager':'','comment':'','ok':None,'file_data':[]}))
    realization_data = TextField(default=pickle.dumps({
	'build':{'smartasr_order':'','date_order':None,'date_tmc':None,'date_doc':None,'date_tmc_out':None,'date_end':None,'sz':'','iss':'','date_real':None,'date_realend':None,'comment':'','author':'','file_data':[]},
	'config':{'smartasr_order':'','date_order':None,'sz':'','date_real':None,'date_realend':None,'comment':'','author':'','file_data':[]},
	'utp':{'smartasr_order':'','date_order':None,'iss':'','date_real':None,'date_realend':None,'comment':'','author':'','file_data':[]}
	}))
    status_data = TextField(default=pickle.dumps([]))
    email_data = TextField(default=pickle.dumps([]))





### --- Создание нового объекта клиента ---
def	NewClient(request,priority,name,address,inn,product,point,service,speed,interface,option,client,email,phone):

    #j = JsonUser(manager)

    db = server['client']

    new = Client(

    priority = priority,
    name = name,
    address = address,
    inn = inn,
    product = product,
    point = point,
#    manager_kod = manager,
#    manager_name = j.j['name2']+' '+j.j['name1'],
#    manager_phone = j.j['phone_office'],

    service = service,
    speed = speed,
    interface = interface,
    option = option,

    client = client,
    email = email,
    phone = phone,

    creator_kod=GetUserKod(request),
    creator_name=GetFio(request),
    creator_phone=GetPhone(request),
    creator_email=GetEmail(request))
    create = datetime.datetime.now()
    doc = new.store(db)

    return doc.id




### --- Список  ---
def	GetList(search):

    db = server['client']

    map_fun = '''function(doc) {
	if(doc._id != 'c83695ba59310ae945108de54b05def1')
	emit(doc._id,[doc.name,doc.address,doc.status,doc.creator_name,doc.creator_phone,doc.create,doc.manager_name,doc.manager_phone,doc.priority]);
    }'''
    data = []

    field = DateTimeField()


    for row in db.query(map_fun):
	if search == '':
	    data.append([
		row.key,
		row.value[0],
		row.value[1],
		row.value[2],
		row.value[3].split()[1]+' '+row.value[3].split()[0],
		row.value[4],
		field._to_python(row.value[5]),
		row.value[6],
		row.value[7],
		row.value[8]
		])
#	elif Compare(row.value[0],search) or Compare(row.value[1],search) or Compare(row.value[2],search) or Compare(row.value[3],search) or Compare(row.value[4],search) or Compare(row.value[6],search) or Compare(row.value[7],search) or Compare(row.value[8],search):
	elif Compare(row.value[0],search) or Compare(row.value[1],search) or Compare(row.value[2],search) or Compare(row.value[3],search) or Compare(row.value[4],search) or Compare(row.value[8],search):
	    data.append([
		row.key,
		row.value[0],
		row.value[1],
		row.value[2],
		row.value[3].split()[1]+' '+row.value[3].split()[0],
		row.value[4],
		field._to_python(row.value[5]),
		row.value[6],
		row.value[7],
		row.value[8]
		])

    data = sorted(data,key=itemgetter(6))
    data.reverse()

    return data





def	GetClient(client_id):

    db = server['client']

    return db[client_id]





def	ClientEdit(client_id,priority,name,address,inn,product,point,service,speed,interface,option,client,email,phone):

#    j = JsonUser(manager)


    db = server['client']
    c = db[client_id]

    c['priority'] = priority
    c['name'] = name
    c['address'] = address
    c['inn'] = inn
    c['product'] = product
    c['point'] = point
#    c['manager_kod'] = manager
#    c['manager_name'] = j.j['name2']+' '+j.j['name1']    
#    c['manager_phone'] = j.j['phone_office']
    c['service'] = service
    c['speed'] = speed
    c['interface'] = interface
    c['option'] = option
    c['client'] = client
    c['email'] = email
    c['phone'] = phone

    db.save(c)





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



### ---
def	GetTech(client_id):

    db = server['client']
    c = db[client_id]

    tech = pickle.loads(c['technical_data'])

    return tech




def	TechEdit(client_id,use,onepay,monthpay,option,jobokp,nemis,comment):

    db = server['client']
    c = db[client_id]

    j = JsonUser(jobokp)

    c['manager_kod'] = jobokp
    c['manager_name'] = j.j['name2']+' '+j.j['name1']    
    c['manager_phone'] = j.j['phone_office']


    tech = pickle.loads(c['technical_data'])
    tech['use'] = use
    tech['onepay'] = onepay
    tech['monthpay'] = monthpay
    tech['option'] = option
    tech['jobokp'] = jobokp
    tech['nemis'] = int(nemis)
    tech['comment'] = comment

    c['technical_data'] = pickle.dumps(tech)

    db.save(c)



### --- Добавление ссылки на файл ---
def	AddOrderFile(client_id,file_str):

    file_id = file_str.split('#')[0]
    file_name = file_str.split('#')[1]

    db = server['client']
    c = db[client_id]
    file_data = pickle.loads(c['file_data'])
    file_data.append([int(time.time()),file_name,file_id])
    c['file_data'] = pickle.dumps(file_data)

    db.save(c)




### --- Список приложенных файлов ---
def	GetOrderFiles(client_id):

    db = server['client']
    c = db[client_id]
    
    return pickle.loads(c['file_data'])



### --- Удаление приложенного файла ---
def	DelOrderFile(client_id,file_id):


    db = server['client']
    c = db[client_id]
    file_data = pickle.loads(c['file_data'])

    for item in file_data:
	if item[0] == int(file_id):
	    file_data.remove(item)

    c['file_data'] = pickle.dumps(file_data)

    db.save(c)






### --- Добавление ссылки на файл ---
def	AddTechFile(client_id,file_str):

    file_id = file_str.split('#')[0]
    file_name = file_str.split('#')[1]

    db = server['client']
    c = db[client_id]
    tech = pickle.loads(c['technical_data'])

    file_data = tech['file_data']
    file_data.append([int(time.time()),file_name,file_id])
    tech['file_data'] = file_data

    c['technical_data'] = pickle.dumps(tech)

    db.save(c)




### --- Список приложенных файлов ---
def	GetTechFiles(client_id):

    db = server['client']
    c = db[client_id]
    tech = pickle.loads(c['technical_data'])
    
    return tech['file_data']



### ---
def	DelTechFile(client_id,file_id):


    db = server['client']
    c = db[client_id]
    tech = pickle.loads(c['technical_data'])

    file_data = tech['file_data']
    for item in file_data:
	if item[0] == int(file_id):
	    file_data.remove(item)

    tech['file_data'] = file_data
    c['technical_data'] = pickle.dumps(tech)

    db.save(c)




### ---
def	GetCom(client_id):

    db = server['client']
    c = db[client_id]

    com = pickle.loads(c['commercial_data'])

    return com



def	ComEdit(client_id,kp,onepay,monthpay,result,manager,comment):

    db = server['client']
    c = db[client_id]
    com = pickle.loads(c['commercial_data'])
    com['kp'] = kp
    com['onepay'] = onepay
    com['monthpay'] = monthpay
    com['result'] = result
    com['manager'] = manager
    com['comment'] = comment

    c['commercial_data'] = pickle.dumps(com)

    db.save(c)



### --- Фиксация, что согласовано ---
def	ComOk(client_id):
    
    db = server['client']
    c = db[client_id]
    com = pickle.loads(c['commercial_data'])
    com['ok'] = True
    c['commercial_data'] = pickle.dumps(com)

    db.save(c)



### --- Добавление ссылки на файл ---
def	AddComFile(client_id,file_str):

    file_id = file_str.split('#')[0]
    file_name = file_str.split('#')[1]

    db = server['client']
    c = db[client_id]
    com = pickle.loads(c['commercial_data'])

    file_data = com['file_data']
    file_data.append([int(time.time()),file_name,file_id])
    com['file_data'] = file_data

    c['commercial_data'] = pickle.dumps(com)

    db.save(c)




### --- Список приложенных файлов ---
def	GetComFiles(client_id):

    db = server['client']
    c = db[client_id]
    com = pickle.loads(c['commercial_data'])
    
    return com['file_data']



### ---
def	DelComFile(client_id,file_id):


    db = server['client']
    c = db[client_id]
    com = pickle.loads(c['commercial_data'])

    file_data = com['file_data']
    for item in file_data:
	if item[0] == int(file_id):
	    file_data.remove(item)

    com['file_data'] = file_data
    c['commercial_data'] = pickle.dumps(com)

    db.save(c)




def	BuildEdit(client_id,smartasr_order,date_order,date_tmc,date_doc,date_tmc_out,date_end,sz,iss,date_real,date_realend,comment,author):

    db = server['client']
    c = db[client_id]
    r = pickle.loads(c['realization_data'])
    b = r['build']
    b['smartasr_order'] = smartasr_order
    b['date_order'] = date_order
    b['date_tmc'] = date_tmc
    b['date_doc'] = date_doc
    b['date_tmc_out'] = date_tmc_out
    b['date_end'] = date_end
    b['sz'] = sz
    b['iss'] = iss
    b['date_real'] = date_real
    b['date_realend'] = date_realend
    b['comment'] = comment
    b['author'] = author

    r['build'] = b
    c['realization_data'] = pickle.dumps(r)

    db.save(c)





def	AddRealFile(real_type,client_id,file_str):

    file_id = file_str.split('#')[0]
    file_name = file_str.split('#')[1]

    db = server['client']
    c = db[client_id]
    r = pickle.loads(c['realization_data'])
    b = r[real_type]
    
    file_data = b['file_data']
    file_data.append([int(time.time()),file_name,file_id])
    b['file_data'] = file_data

    r[real_type] = b
    c['realization_data'] = pickle.dumps(r)

    db.save(c)




### --- Список приложенных файлов ---
def	GetRealFiles(real_type,client_id):

    db = server['client']
    c = db[client_id]
    r = pickle.loads(c['realization_data'])
    b = r[real_type]
    

    return b['file_data']




### --- 
def	DelRealFile(real_type,client_id,file_id):


    db = server['client']
    c = db[client_id]
    b = pickle.loads(c['realization_data'])

    r = b[real_type]
    file_data = r['file_data']
    for item in file_data:
	if item[0] == int(file_id):
	    file_data.remove(item)

    r['file_data'] = file_data
    b[real_type] = r
    c['realization_data'] = pickle.dumps(b)

    db.save(c)




def	ConfigEdit(client_id,smartasr_order,date_order,sz,date_real,date_realend,comment,author):

    db = server['client']
    c = db[client_id]
    r = pickle.loads(c['realization_data'])
    b = r['config']
    b['smartasr_order'] = smartasr_order
    b['date_order'] = date_order
    b['sz'] = sz
    b['date_real'] = date_real
    b['date_realend'] = date_realend
    b['comment'] = comment
    b['author'] = author

    r['config'] = b
    c['realization_data'] = pickle.dumps(r)

    db.save(c)



def	UTPEdit(client_id,smartasr_order,date_order,iss,date_real,date_realend,comment,author):

    db = server['client']
    c = db[client_id]
    r = pickle.loads(c['realization_data'])
    b = r['utp']
    b['smartasr_order'] = smartasr_order
    b['date_order'] = date_order
    b['iss'] = iss
    b['date_real'] = date_real
    b['date_realend'] = date_realend
    b['comment'] = comment
    b['author'] = author

    r['utp'] = b
    c['realization_data'] = pickle.dumps(r)

    db.save(c)





### --- Формирование правил email рассылки ---
def	AddEmailUser(request,user_id,status):

    j = JsonUser(user_id)

    user_name = j.j['name2']+' '+j.j['name1']    
    user_email = j.j['email']

    author = GetFio(request)
    author_name = author.split()[1]+' '+author.split()[0]

    db = server['client']
    c = db['c83695ba59310ae945108de54b05def1']


    l = pickle.loads(c['email_list'])

    li = []
    for item in l:
	li.append(item['user_id']+item['status'])
    if li.count(user_id+status) == 0:
	l.append({
	    'id':int(time.time()),
	    'date':datetime.datetime.now(),
	    'status':status,
	    'user':user_name,
	    'user_id':user_id,
	    'email':user_email,
	    'author':author_name
	    })


    c['email_list'] = pickle.dumps(l)

    db.save(c)



### --- Вывод истоиии email уведомелний ---
def	GetEmailHistory(client_id):

    db = server['client']
    c = db[client_id]
    l = pickle.loads(c['email_data'])
    
    return l





### --- вывод списка настроек email рассылки ---
def	GetEmailUser():

    db = server['client']
    c = db['c83695ba59310ae945108de54b05def1']
    l = pickle.loads(c['email_list'])

    return l



### --- Удаление адреса рассылки ---
def	DelEmailUser(rec_id):


    db = server['client']
    c = db['c83695ba59310ae945108de54b05def1']


    l = pickle.loads(c['email_list'])

    for item in l:
	if item['id'] == int(rec_id):
	    l.remove(item)


    c['email_list'] = pickle.dumps(l)

    db.save(c)




## --- Принято в работу ---
def	InWork(request,client_id):

    author = GetFio(request)
    author_name = author.split()[1]+' '+author.split()[0]

    db = server['client']
    c = db[client_id]
    c['in_work'] = author_name

    db.save(c)



## --- Принято в реализацию ---
def	InReal(request,client_id):

    author = GetFio(request)
    author_name = author.split()[1]+' '+author.split()[0]

    db = server['client']
    c = db[client_id]
    c['in_real'] = author_name

    db.save(c)



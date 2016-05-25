#coding:utf-8

from	django.db	import	connections, transaction
import	base64
import	pickle
import	time
import	datetime

from	decimal	import	*

from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField, DecimalField
from	jsondata	import	UserEmailList,UserList,JsonUser
from	userdata	import	GetEmail,GetPhone,GetFio,GetUserKod

from	common		import	Compare

server = Server()


class	Contract(Document):
    author = TextField()
    author_name = TextField()
    author_phone = TextField()
    author_email = TextField()
    contragent = TextField()
    tema = TextField()
    block = TextField()
    contract = TextField()
    file_data = TextField(default=pickle.dumps({'file_link':'','file_name':'','file_ext':''}))
    order_data = TextField(default=pickle.dumps([]))
    added = DateTimeField(default=datetime.datetime.now())
    summ = DecimalField(default=0)


class	ContractData(Document):
    data = TextField()


def	NewContract(request,contragent,tema,block,contract,file_name,data,file_ext):


    db = server['costcontract']
    db2 = server['costcontractdata']

    if file_name != '':
	filedata = ContractData(data=data)
	doc = filedata.store(db2)
	doc_id = doc.id
    else:
	doc_id = ''

    con = Contract(
	author=GetUserKod(request),
	author_name=GetFio(request),
	author_phone=GetPhone(request),
	author_email=GetEmail(request),
	contragent=contragent,
	contract=contract,
	tema=tema,
	block=block,
	file_data=pickle.dumps({'file_link':doc_id,'file_name':file_name,'file_ext':file_ext}),
	added = datetime.datetime.now()
	)
    con.store(db)




def	ListContract(search):

    db = server['costcontract']
    map_fun = '''function(doc) {
	    emit(doc._id,[doc.contragent,doc.contract,doc.tema,doc.block,doc.author_name,doc.author_phone,doc.summ,doc.added]);
    }'''

    data = []

    field = DateTimeField()

    for row in db.query(map_fun):
	author = row.value[4].split()[1].encode('utf-8')+' '+row.value[4].split()[0].encode('utf-8')
	if search == '':
	    data.append({
		'rec_id':row.key,
		'contragent':row.value[0].encode('utf-8'),
		'contract':row.value[1].encode('utf-8'),
		'tema':row.value[2].encode('utf-8'),
		'block':row.value[3].encode('utf-8'),
		'author':author,
		'phone':row.value[5].encode('utf-8'),
		'sum':row.value[6],
		'added':field._to_python(row.value[7])
		})
	else:
	    if Compare(row.value[0],search) or Compare(row.value[1],search) or Compare(row.value[2],search) or Compare(row.value[3],search) or Compare(author.decode('utf-8'),search):
		data.append({
		    'rec_id':row.key,
		    'contragent':row.value[0].encode('utf-8'),
		    'contract':row.value[1].encode('utf-8'),
		    'tema':row.value[2].encode('utf-8'),
		    'block':row.value[3].encode('utf-8'),
		    'author':author,
		    'phone':row.value[5].encode('utf-8'),
		    'sum':row.value[6],
		    'added':field._to_python(row.value[7])
		    })

    return data




### --- Получение договора ---
def	GetContract(contract_id):

    db = server['costcontract']

    return db[contract_id]




### --- Редактирование договора ---
def	EditContract(contract_id,contragent,tema,block,contract,file_name,data,file_ext):



    db = server['costcontract']
    c = db[contract_id]

    file_data = pickle.loads(c['file_data'])

    c['contragent'] = contragent
    c['tema'] = tema
    c['block'] = block
    c['contract'] = contract

    if file_name != '' and file_data['file_link'] != '':
	db2 = server['costcontractdata']
	f = db2[file_data['file_link']]
	f['data'] = data
	db2.save(f)
	file_data['file_name'] = file_name
	file_data['file_ext'] = file_ext
	c['file_data'] = pickle.dumps(file_data)

    elif file_name != '' and file_data['file_link'] == '':
	db2 = server['costcontractdata']
	filedata = ContractData(data=data)
	doc = filedata.store(db2)
	doc_id = doc.id
	file_data['file_link'] = doc_id
	file_data['file_name'] = file_name
	file_data['file_ext'] = file_ext
	c['file_data'] = pickle.dumps(file_data)

    db.save(c)



### --- Файл договора ---
def	GetFileData(contract_id,file_id):

    f = {}
    
    db = server['costcontract']
    db2 = server['costcontractdata']

    fd = db2[file_id]

    c = db[contract_id]
    file_data = pickle.loads(c['file_data'])
    f['filename'] = file_data['file_name']
    f['ext'] = file_data['file_ext']
    f['data'] = fd['data']

    return f




### --- Добавление заказа ---
def	AddOrder(request,contract_id,order_name,cost,start_date,end_date,clientorder,status,file_name,data,file_ext):


    author = GetFio(request)
    author_name = author.split()[1]+' '+author.split()[0]

    db = server['costcontract']
    c = db[contract_id]

    order_data = pickle.loads(c['order_data'])

    order = {}
    order['order_id'] = int(time.time())
    order['order'] = order_name
    order['cost'] = cost
    order['start_date'] = start_date
    order['end_date'] = end_date
    order['clientorder'] = clientorder
    order['status'] = status
    order['create'] = datetime.datetime.now()
    order['author'] = author_name
    
    if file_name == '':
	order['file_link'] = ''
    else:
	db2 = server['costcontractdata']
	filedata = ContractData(data=data)
	doc = filedata.store(db2)
	doc_id = doc.id
	order['file_link'] = doc_id

    order['file_name'] = file_name
    order['file_ext'] = file_ext

    order_data.append(order)
    
    doc_sum = Decimal('0.00')
    ### --- расчет суммы ---
    for item in order_data:
	if item['status'] == u'Активный':
	    doc_sum = doc_sum + Decimal(item['cost'])

    c['summ'] = float(doc_sum)
    c['order_data'] = pickle.dumps(order_data)

    db.save(c)






### --- Файл заказа  ---
def	GetFileOrderData(contract_id,order_id):

    f = {}
    
    db = server['costcontract']
    db2 = server['costcontractdata']


    c = db[contract_id]
    order_data = pickle.loads(c['order_data'])

    for item in order_data:
	if item['order_id'] == int(order_id):

	    f['filename'] = item['file_name']
	    f['ext'] = item['file_ext']
	    fd = db2[item['file_link']]
	    f['data'] = fd['data']
	    return f



### --- Данные заказа ---
def	GetOrderData(contract_id,order_id):

    db = server['costcontract']
    c = db[contract_id]
    order_data = pickle.loads(c['order_data'])

    for item in order_data:
	if item['order_id'] == int(order_id):
	    return item




### --- Изменение заказа ---
def	EditOrder(contract_id,order_id,order_name,cost,start_date,end_date,clientorder,status,file_name,data,file_ext):

#    getcontext().prec = 6

    db = server['costcontract']
    c = db[contract_id]

    order_data = pickle.loads(c['order_data'])

    for item in order_data:
	if item['order_id'] == int(order_id):
	    i = order_data.index(item)
	    item['order'] = order_name
	    item['cost'] = Decimal(cost)
	    item['start_date'] = start_date
	    item['end_date'] = end_date
	    item['clientorder'] = clientorder
	    item['status'] = status

    
	    if file_name != '' and item['file_link'] =='':
		db2 = server['costcontractdata']
		filedata = ContractData(data=data)
		doc = filedata.store(db2)
		doc_id = doc.id
		item['file_link'] = doc_id
		item['file_name'] = file_name
		item['file_ext'] = file_ext
	    elif file_name != '' and item['file_link'] !='':
		db2 = server['costcontractdata']
		f = db2[item['file_link']]
		f['data'] = data
		db2.save(f)
		item['file_name'] = file_name
		item['file_ext'] = file_ext

	    order_data[i] = item

    
    doc_sum = Decimal('0.00')
    ### --- расчет суммы ---
    for item in order_data:
	if item['status'] == u'Активный':
	    doc_sum = doc_sum + Decimal(item['cost'])


    c['summ'] = float(doc_sum)
    c['order_data'] = pickle.dumps(order_data)

    db.save(c)




### --- Удаление контракта ---
def	DelOrder(contract_id,order_id):


    db = server['costcontract']
    c = db[contract_id]

    order_data = pickle.loads(c['order_data'])

    for item in order_data:
	if item['order_id'] == int(order_id):
	    if item['file_link'] !='':
		db2 = server['costcontractdata']
		f = db2[item['file_link']]
		db2.delete(f)
	    order_data.remove(item)

    doc_sum = Decimal('0.00')
    ### --- расчет суммы ---
    for item in order_data:
	if item['status'] == u'Активный':
	    doc_sum = doc_sum + item['cost']

    c['summ'] = float(doc_sum)


    c['order_data'] = pickle.dumps(order_data)

    db.save(c)

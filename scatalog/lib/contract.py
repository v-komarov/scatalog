#coding:utf-8

from	django.db	import	connections, transaction
import	base64



import	datetime

from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField
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
    comment = TextField()
    filename = TextField()
    data_id = TextField()
    ext = TextField()
    kis_id = IntegerField(default=0)
    added = DateTimeField(default=datetime.datetime.now())



class	ContractData(Document):
    data = TextField()



def	NewContract(request,contragent,comment,filename,data,ext):


    db = server['contracts']
    db2 = server['contractdata']

    filedata = ContractData(data=data)
    doc = filedata.store(db2)

    con = Contract(author=GetUserKod(request),author_name=GetFio(request),author_phone=GetPhone(request),author_email=GetEmail(request),contragent=contragent,comment=comment,filename=filename,data_id=doc.id,ext=ext)
    con.store(db)




def	ListContract(search):

    db = server['contracts']
    map_fun = '''function(doc) {
	    emit(doc._id,[doc.filename,doc.contragent,doc.comment,doc.author_name,doc.added,doc.kis_id]);
    }'''

    data = []

    field = DateTimeField()

    for row in db.query(map_fun):
	author = row.value[3].split()[1]+u' '+row.value[3].split()[0]
	if search == '':
	    data.append([row.key,
	    row.value[0].encode('utf-8'),
	    row.value[1].encode('utf-8'),
	    row.value[2].encode('utf-8'),
	    author.encode('utf-8'),
	    field._to_python(row.value[4]),
	    row.value[5]])
	else:
	    if Compare(row.value[0],search) or Compare(row.value[1],search) or Compare(row.value[2],search) or Compare(row.value[3],search):
		data.append([row.key,
		row.value[0].encode('utf-8'),
		row.value[1].encode('utf-8'),
		row.value[2].encode('utf-8'),
		author.encode('utf-8'),
		field._to_python(row.value[4]),
		row.value[5]])
    return data





def	GetContractData(contract_id):


    db = server['contracts']
    db2 = server['contractdata']
    
    c = db[contract_id]
    d = db2[c['data_id']]

    c['data_id'] = d['data']

    return c




def	DelContract(contract_id):

    db = server['contracts']
    db2 = server['contractdata']
    
    doc = db[contract_id]
    data = db2[doc['data_id']]
    db2.delete(data)
    db.delete(doc)



### --- Список номеров заявок КИС загруженных в базу ---
def	ListDCod():

    db = server['contracts']
    map_fun = '''function(doc) {
	if (doc.kis_id != 0)
	    emit(doc._id,doc.kis_id);
    }'''

    data = []

    for row in db.query(map_fun):
	data.append(row.value)

    
    return data




def	GetDList():

    cursor = connections['kis'].cursor()
    cursor.execute("SELECT t_rec_id,t_contragent,t_tema,right(t_file_name,50),t_ext,t_doc_data,right(t_app_filename,50),t_app_ext,t_app_data FROM t_d WHERE t_rec_delete=0 AND t_dstatus_kod=5;")
    data = cursor.fetchall()

    listkis = ListDCod()

    for row in data:

	try:
	    listkis.index(row[0])
	except:
	    
	    db = server['contracts']
	    db2 = server['contractdata']

	    filedata = ContractData(data=base64.b64encode(row[5]))
	    doc = filedata.store(db2)
	    con = Contract(author=u'',author_name=u'Заявки Договоры',author_phone=u'',author_email=u'',contragent=row[1],comment=row[2],filename=row[3],ext=row[4],data_id=doc.id,kis_id=row[0])
	    con.store(db)

	    ### --- Добавление приложения ---
	    if row[6] != '':
		filedata = ContractData(data=base64.b64encode(row[8]))
		doc = filedata.store(db2)
		con = Contract(author=u'',author_name=u'Заявки Договоры',author_phone=u'',author_email=u'',contragent=row[1],comment=row[2],filename=row[6],ext=row[7],data_id=doc.id,kis_id=row[0])
		con.store(db)


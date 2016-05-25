#coding:utf-8

import	datetime
import	cPickle


from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField, BooleanField
from	jsondata	import	UserEmailList,UserList,JsonUser
from	userdata	import	GetEmail,GetPhone,GetFio,GetUserKod


server = Server()


class	Scheme(Document):
    scheme_id = IntegerField()
    scheme_name = TextField()
    author = TextField()
    author_name = TextField()
    author_phone = TextField()
    author_email = TextField()
    added = DateTimeField(default=datetime.datetime.now())
    step_data = TextField(default=cPickle.dumps([]))
    attrs_list = ListField(TextField())




### --- Определение scheme_id ---
def	NextSchemeId():

    db = server['scheme']
    map_fun = '''function(doc) {
	emit(doc._id,doc.scheme_id);
    }'''

    data = []

    for row in db.query(map_fun):
	data.append(row.value)

    if len(data) == 0:
	return 1
    else:
	sorted(data)
	return data[-1]+1



### --- Создание новой схемы ---
def	CreateScheme(request,name):

    db = server['scheme']

    newscheme = Scheme(
    scheme_name=name,
    
    scheme_id=NextSchemeId(),
    author=GetUserKod(request),
    author_name=GetFio(request),
    author_phone=GetPhone(request),
    author_email=GetEmail(request))
    doc = newscheme.store(db)

    return doc.id



### --- Список схем ---
def	GetSchemeList():

    db = server['scheme']
    map_fun = '''function(doc) {
	emit(doc.scheme_id,[doc._id,doc.scheme_name,doc.author_name,doc.added,doc.attrs_list]);
    }'''

    data = []

    field = DateTimeField()

    for row in db.query(map_fun):
	data.append([row.key,row.value[0],row.value[1],row.value[2].split()[1]+' '+row.value[2].split()[0],field._to_python(row.value[3]),row.value[4]])

    sorted(data)


    return data




### --- Считываем схему из базы в списки  ---
def	GetSchemeData(scheme_id):

    scheme_db = server['scheme']
    scheme = scheme_db[scheme_id]

    data = {}
    data['name'] = scheme['scheme_name']
    data['stepdata'] = cPickle.loads(scheme['step_data'].encode('utf-8'))

    return data





### --- Сохранение схемы ---
def	SaveScheme(data):

    scheme_id = data['scheme_id']
    stepdata = data['stepdata']
    scheme_name = data['name']

    db = server['scheme']
    doc = db[scheme_id]
    doc['step_data'] = cPickle.dumps(stepdata)
    doc['scheme_name'] = scheme_name

    db.save(doc)

    return 'OK'




### --- Добавление атрибута ---
def	AddAttr(scheme_id,attr):

    db = server['scheme']
    scheme = db[scheme_id]
    attrs = scheme['attrs_list']


    if attrs.count(attr) == 0:
	attrs.append(attr)
	scheme['attrs_list'] = attrs
	db.save(scheme)

    return 'OK'


### --- Список атрибутов по схеме ---
def	AttrList(scheme_id):
    
    db = server['scheme']
    scheme = db[scheme_id]
    
    return scheme['attrs_list']




### --- Удаление атрибута ---
def	DelAttr(scheme_id,attr):

    db = server['scheme']
    scheme = db[scheme_id]
    attrs = scheme['attrs_list']


    attrs.remove(attr)
    scheme['attrs_list'] = attrs
    db.save(scheme)

    return 'OK'

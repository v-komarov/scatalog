#coding:utf-8

import	datetime

from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField
from	jsondata	import	UserEmailList,UserList,JsonUser
from	userdata	import	GetEmail,GetPhone,GetFio
from	userfiles_mail	import	FileLinkAccess

from	common		import	Compare

server = Server()


class	MyFile(Document):
    author = TextField()
    author_name = TextField()
    author_phone = TextField()
    author_email = TextField()
    comment = TextField()
    filename = TextField()
    filesize = IntegerField()
    data_id = TextField()
    ext = TextField()
    access = TextField()
    users = ListField(ListField(TextField()))
    added = DateTimeField(default=datetime.datetime.now())



class	MyData(Document):
    data = TextField()




def	NewFile(author,author_name,author_phone,author_email,comment,filename,data,ext,size):

    db = server['userfiles']
    db2 = server['userdata']

    mydata = MyData(data=data)
    doc = mydata.store(db2)

    myfile = MyFile(author=author,author_name=author_name,author_phone=author_phone,author_email=author_email,comment=comment,filename=filename,data_id=doc.id,ext=ext,access='private',users='',filesize=size)
    myfile.store(db)



def	ListFile(author,search):
    author = author.encode("utf-8")

    db = server['userfiles']
    map_fun = '''function(doc) {
	if (doc.author == '%s')
	    emit(doc._id,[doc.filename,doc.comment,doc.access,doc.added,doc.filesize]);
    }''' % author

    data = []

    field = DateTimeField()

    for row in db.query(map_fun):
	if search == '':
	    data.append([row.key,row.value[0].encode('utf-8'),row.value[1].encode('utf-8'),row.value[2].encode('utf-8'),field._to_python(row.value[3]),row.value[4]])
	else:
	    if Compare(row.value[0],search) or Compare(row.value[1],search):
		data.append([row.key,row.value[0].encode('utf-8'),row.value[1].encode('utf-8'),row.value[2].encode('utf-8'),field._to_python(row.value[3]),row.value[4]])
    return data



def	GetFileData(file_id):


    db = server['userfiles']
    db2 = server['userdata']
    
    f = db[file_id]
    d = db2[f['data_id']]

    f['data_id'] = d['data']

    return f




def	DelFile(file_id):

    db = server['userfiles']
    db2 = server['userdata']
    
    doc = db[file_id]
    data = db2[doc['data_id']]
    db2.delete(data)
    db.delete(doc)




### --- Список email адресов ---
def	GetEmailList():

    e = UserEmailList()
    
    l = []
    data = []

    for key in e.j.keys():
	l.append(e.j[key]+'#'+key)

    l.sort()
    for row in l:
	data.append([row.split('#')[1],row.split('#')[0]])

    return data




def	SetTypeAccess(file_id,access):

    db = server['userfiles']
    doc = db[file_id]
    doc['access'] = access
    db.save(doc)



### --- Список для выбора пользователя ---
def	GetUserList():

    e = UserList()
    
    l = []
    data = []

    for key in e.j.keys():
	l.append(e.j[key][2]+' '+e.j[key][1]+'#'+key)

    l.sort()
    for row in l:
	data.append([row.split('#')[1],row.split('#')[0]])

    return data




### --- Список пользователей, которым предоставлен доступ ---
def	GetAccessUser(file_id):
    
    db = server['userfiles']
    doc = db[file_id]
    users = doc['users']

    return users





### --- Данные пользователя (по коду) ---
def	AddUserData(user_id,file_id,request):
    j = JsonUser(user_id)

    db = server['userfiles']
    doc = db[file_id]
    users = doc['users']
    users.append([j.j['user_id'],j.j['name1'],j.j['name2'],j.j['name3'],j.j['email']])
    doc['users'] = users
    db.save(doc)

    FileLinkAccess(j.j['email'],GetEmail(request),doc['comment'],doc['filename'],file_id)



### --- Удаление пользователя из списка доступа ---
def	DelUserAccess(user_id,file_id):
    db = server['userfiles']
    doc = db[file_id]
    users = doc['users']

    for item in users:
	if item[0] == user_id:
	    users.remove(item)
    doc['users'] = users
    db.save(doc)





def	ListOtherFile(author,search):
    author = author.encode("utf-8")


    db = server['userfiles']
    map_fun = '''function(doc) {
	    if (doc.access == "public" && doc.author != '%s')
	    emit(doc._id,[doc.filename,doc.comment,doc.author,doc.author_name,doc.author_phone,doc.added,doc.filesize]);
    }''' % author


    data = []

    field = DateTimeField()

    for row in db.query(map_fun):
	if search == '':
	    data.append([row.key,row.value[0].encode('utf-8'),row.value[1].encode('utf-8'),row.value[2].encode('utf-8'),row.value[3].encode('utf-8').split(' ')[1],row.value[3].encode('utf-8').split(' ')[0],row.value[4].encode('utf-8'),field._to_python(row.value[5]),row.value[6]])
	else:
	    if Compare(row.value[0],search) or Compare(row.value[1],search):
		data.append([row.key,row.value[0].encode('utf-8'),row.value[1].encode('utf-8'),row.value[2].encode('utf-8'),row.value[3].encode('utf-8').split(' ')[1],row.value[3].encode('utf-8').split(' ')[0],row.value[4].encode('utf-8'),field._to_python(row.value[5]),row.value[6]])
    return data




def	SaveComment(file_id,comment):

    db = server['userfiles']
    doc = db[file_id]
    doc['comment'] = comment
    db.save(doc)


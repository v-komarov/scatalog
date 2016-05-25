#coding:utf-8

import	datetime

from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField


server = Server()


class	MyFile(Document):
    author = TextField()
    author_name = TextField()
    author_phone = TextField()
    author_email = TextField()
    comment = TextField()
    filename = TextField()
    data = TextField()
    ext = TextField()
    access = TextField()
    users = ListField(ListField(TextField()))
    added = DateTimeField(default=datetime.datetime.now())




def	SetAdded():
    
    db = server['userfiles']
    map_fun = '''function(doc) {
	if (1)
	    emit(doc._id,[doc.filename]);
    }'''




    for row in db.query(map_fun):
	doc = db[row.key]
	myfile = MyFile(author=doc['author'],author_name=doc['author_name'],author_phone=doc['author_phone'],author_email=doc['author_email'],comment=doc['comment'],filename=doc['filename'],data=doc['data'],ext=['ext'],access=doc['access'],users=doc['users'])
	myfile.store(db)



def	Erlang():

    db = server['userfiles']

    map_fun = '''
	fun({Doc}) ->
	Id = proplists:get_value(<<_id>>,Doc,null),
	Author = proplists:get_value(<<author>>,Doc,null),
	Emit([Id],[Author])
	end.
    '''

    map_fun = '''fun() -> Emit(null,null) end.'''.encode('utf-8')


    for row in db.query(map_fun):
	print row.key


#coding:utf-8

import	datetime
import	pickle
import	time

from	operator	import	itemgetter

from	clients		import	Client

from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField, BooleanField
from	jsondata	import	UserEmailList,UserList,JsonUser
from	userdata	import	GetEmail,GetPhone,GetFio,GetUserKod

from	clients_mail	import	StatusInfo

server = Server()




### --- Пишем историю статусов ---
def	StatusHistory(client_id,status,request):


    author = GetFio(request)
    author_name = author.split()[1]+' '+author.split()[0]
    phone = GetPhone(request)



    db = server['client']
    c = db[client_id]
    s = pickle.loads(c['status_data'])


    status_list = []
    for item in s:
	status_list.append(item['status'])

    if status_list.count(status) == 0:
	s.append({'date':datetime.datetime.now(),'status':status,'author':author_name,'phone':phone})
	mail_log = StatusInfo(request,client_id,status)

	data = pickle.loads(c['email_data'])
	data.append(mail_log)
	c['email_data'] = pickle.dumps(data)

    c['status'] = status.decode('utf-8')
    c['status_data'] = pickle.dumps(s)

    db.save(c)



### --- Список истории статусов ---
def	GetStatusHistory(client_id):

    db = server['client']
    c = db[client_id]
    s = pickle.loads(c['status_data'])

    #data =s.reverse()

    return s


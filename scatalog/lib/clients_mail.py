#coding:utf-8

from	django.db		import	connections, transaction
from	django.core.mail	import	send_mail

from	couchdb	import	Server
import	pickle
import	datetime

from	userdata	import	GetEmail,GetPhone,GetFio,GetUserKod

server = Server()



### --- Сообщение о статусе ---
def	StatusInfo(request,client_id,status):

    db = server['client']
    c = db[client_id]

    email_list = []
    o = db['c83695ba59310ae945108de54b05def1']
    l = pickle.loads(o['email_list'])
    for item in l:
	if item['status'].encode('utf-8') == status:
	    email_list.append(item['email'])

    if email_list.count(c['creator_email']) == 0:
	email_list.append(c['creator_email'])


    m = u"""\
    Подключение клиентов %s\n\
    Информация о статусе\n\
    Текущий статус %s\n\
    \n\n\
    Ссылка http://10.6.1.10:8000/client/?client_id=%s\n\n\
    """ % (c['name'],c['status'],client_id)
    send_mail('SCatalog',m,GetEmail(request),email_list)


    mail_log = {
	'date':datetime.datetime.now(),
	'mail':email_list,
	'info':'Уведомление o статусе : %s' % status
    }

#    data = pickle.loads(c['email_data'])
#    data.append(mail_log)
#    c['email_data'] = pickle.dumps(data)
    
#    db.save(c)

    return mail_log


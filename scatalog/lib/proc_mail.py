#coding:utf-8

from	django.db		import	connections, transaction
from	django.core.mail	import	send_mail

from	couchdb	import	Server

from	proc	import	NextPerson
from	userdata	import	GetEmail

import	datetime
import	pickle

server = Server()


### --- Сообщение следующему согласующему ---
def	SendNextPerson(request,proc_id):

    db = server['proc']
    proc = db[proc_id]

    person = NextPerson(proc_id)

    ### --- Проверка статуса процесса ---
    if proc['status'] != u'Выполняется' or person['email'] == u'':
	return 'ERROR'


    m = u"""\
    Ваша очередь согласования процесса № %s %s\n\
    \n\n\
    Ссылка http://10.6.1.10:8000/procstep/?proc_id=%s\n\n\
    """ % (proc['proc_num'],proc['proc_name'],proc['_id'])
    send_mail('SCatalog',m,GetEmail(request),[person['email'],])


    mail_log = {
	'date':datetime.datetime.now(),
	'mail':GetEmail(request),
	'info':'Уведомление согласующему'
    }

    data = pickle.loads(proc['email_data'])
    data.append(mail_log)
    proc['email_data'] = pickle.dumps(data)
    
    db.save(proc)




### --- Сообщение о новом комментарии / файле ---
def	SendComment(request,proc_id,comment,file_link):


    db = server['proc']
    proc = db[proc_id]

    user = GetEmail(request)

    ### --- Проверка статуса процесса ---
    if proc['status'] == u'Выполняется':

	### --- Список рассылки ---
	emails = []
	scheme_link = proc['scheme_link']
	dbs = server['scheme']
	scheme = dbs[scheme_link]
	data = pickle.loads(scheme['step_data'])
	for item in data:
	    if emails.count(item['user_email']) == 0 and user != item['user_email']:
	    #if True:
		emails.append(item['user_email'])

	if emails.count(proc['author_email']) == 0 and proc['author_email'] != user:
	    emails.append(proc['author_email'])

	if file_link == '#':
	    file_n = ''
	    file_l = ''
	else:
	    file_n = file_link.split('#')[1]
	    file_l = 'http://10.6.1.10:8000/getfile?file_id=%s' % file_link.split('#')[0]

	m = u"""\
	Процесс № %s %s\n\
	Добавлен комметарий:\n\
	%s
	\n\n\
	Файл:\n\
	%s\n\
	%s\n\
	\n\n\
	Ссылка http://10.6.1.10:8000/proccomment/?proc_id=%s\n\n\
	""" % (proc['proc_num'],proc['proc_name'],comment,file_n,file_l,proc['_id'])
	send_mail('SCatalog',m,user,emails)

	e = ' '.join(emails)
	
	if len(emails)!=0:

	    mail_log = {
		'date':datetime.datetime.now(),
		'mail':e,
		'info':'Добавление комментария'
	    }

	    data = pickle.loads(proc['email_data'])
	    data.append(mail_log)
	    proc['email_data'] = pickle.dumps(data)
    
	    db.save(proc)




### --- Уведомление, что процесс завершен ---
def	ProcOver(proc_id):

    db = server['proc']
    proc = db[proc_id]

    author_email = proc['author_email']



    m = u"""\
    Процесс согласования № %s %s\n\
    \n\n\
    Ссылка http://10.6.1.10:8000/procstep/?proc_id=%s\n\n\
    Завершен.
    """ % (proc['proc_num'],proc['proc_name'],proc['_id'])
    send_mail('SCatalog',m,GetEmail(request),[author_email,])


    mail_log = {
	'date':datetime.datetime.now(),
	'mail':GetEmail(request),
	'info':'Процесс завершен'
    }

    data = pickle.loads(proc['email_data'])
    data.append(mail_log)
    proc['email_data'] = pickle.dumps(data)
    
    db.save(proc)



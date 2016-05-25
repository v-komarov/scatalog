#coding:utf-8

from	django.db		import	connections, transaction
from	django.core.mail	import	send_mail



### --- Отправка ссылки на файл ---
def	FileLink(email,author_email,comment,filename,file_id):

    m = u"""\
    Ссылка на файл\n\
    %s\n\n\
    Ссылка http://10.6.1.10:8000/getfile?file_id=%s\n\n\
    Комментарий: %s\n\
    """ % (filename,file_id,comment)
    send_mail('SCatalog-File',m,author_email,[email,])



### --- Отправка ссылки на файл ---
def	FileLinkAccess(email,author_email,info,filename,file_id):

    m = u"""\
    Вам предоставлен доступ\n\n\
    Ссылка на файл\n\
    %s\n\n\
    Ссылка http://10.6.1.10:8000/getfile?file_id=%s\n\n\
    Описание файла: %s\n\
    """ % (filename,file_id,info)
    send_mail('SCatalog-File',m,author_email,[email,])


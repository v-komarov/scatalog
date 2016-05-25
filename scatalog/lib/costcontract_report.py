#coding:utf-8

from	django.db	import	connections, transaction
import	base64
import	pickle
import	time
import	datetime
import	xlwt


from	couchdb	import	Server
from	couchdb.mapping	import	Document, TextField, ListField, DateTimeField, IntegerField
from	jsondata	import	UserEmailList,UserList,JsonUser
from	userdata	import	GetEmail,GetPhone,GetFio,GetUserKod

from	common		import	Compare

server = Server()


### --- Отчет 1 ---
def	Report1(tema,contragent):

    db = server['costcontract']
    if tema == '' and contragent == '':

        map_fun = '''function(doc) {
		emit(doc._id,doc.order_data);
	}'''
    elif tema != '' and contragent == '':

        map_fun = '''function(doc) {
		if (doc.tema == '%s')
		emit(doc._id,doc.order_data);
	}''' % tema

    elif tema == '' and contragent != '':

        map_fun = '''function(doc) {
		if (doc.contragent == '%s')
		emit(doc._id,doc.order_data);
	}''' % contragent

    else:
        map_fun = '''function(doc) {
		if (doc.contragent == '%s' && doc.tema == '%s')
		emit(doc._id,doc.order_data);
	}''' % (contragent,tema)

    s = 0

    for row in db.query(map_fun):
	order_data = pickle.loads(row.value)
	for item in order_data:
	    if item['status'] == u'Активный':
		s = s + item['cost']
    print s
    return s



### --- Список контрагентов ---
def	GetContragentList(): 

    db = server['costcontract']
    map_fun = '''function(doc) {
	    emit(doc._id,doc.contragent);
    }'''

    c = []

    for row in db.query(map_fun):
	if c.count(row.value) == 0:
	    c.append(row.value)

    return c






### --- Выгрузка базы в Excel  ---
def	Data2Excel(response):


    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Contracts')

    default_style = xlwt.Style.default_style

    sheet.col(0).width = 256*50
    sheet.col(1).width = 256*10
    sheet.col(2).width = 256*30
    sheet.col(3).width = 256*10
    sheet.col(4).width = 256*30
    sheet.col(5).width = 256*20
    sheet.col(6).width = 256*10
    sheet.col(7).width = 256*20
    sheet.col(8).width = 256*10
    sheet.col(9).width = 256*20
    sheet.col(10).width = 256*20
    sheet.col(11).width = 256*20
    sheet.col(12).width = 256*20
    
    style = xlwt.easyxf('font: bold 1')

    sheet.write(0,0,'Контрагент',style)
    sheet.write(0,1,'Номер договора',style)
    sheet.write(0,2,'Тема',style)
    sheet.write(0,3,'Сумма',style)
    sheet.write(0,4,'Исполнитель',style)
    sheet.write(0,5,'Принадлежность',style)
    sheet.write(0,6,'Создан',style)
    sheet.write(0,7,'Номер заказа',style)
    sheet.write(0,8,'Еж.м.платежи',style)
    sheet.write(0,9,'Начало реализации',style)
    sheet.write(0,10,'Окончание реализации',style)
    sheet.write(0,11,'Клиентский заказ',style)
    sheet.write(0,12,'Статус',style)




    db = server['costcontract']
    map_fun = '''function(doc) {
	    emit(doc._id,doc.contragent);
    }'''

    c = []

    for row in db.query(map_fun):
	if c.count(row.value) == 0:
	    c.append(row.value)



#    data = GetReportSpecData(chief,start_date,end_date)

#    i = 1
#    for row in data:
#	sheet.write(i,0,row[8])
#	sheet.write(i,1,row[0])
#	sheet.write(i,2,row[3])
#	sheet.write(i,3,row[4])
#	sheet.write(i,4,row[5])
#	sheet.write(i,5,row[6])
#	sheet.write(i,6,row[7])
#	sheet.write(i,7,row[9]+' '+row[10])
#	sheet.write(i,8,row[11]+' '+row[12])
#	i = i + 1
    
    

    book.save(response)
    return response



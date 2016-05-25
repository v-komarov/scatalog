#coding:utf-8
from	django.http	import	HttpResponse
import	json
import	urllib2


url = 'http://10.6.0.223:20000/userdataservice/?'


### --- Данные в формате json ---
class	JsonUser():

    def	__init__(self,user_id):

	self.url = "%suser_id=%s" % (url,user_id)
	self.json_str = urllib2.urlopen(self.url).read()
	self.json_str = self.json_str.encode("utf-8")

	self.j = json.loads(self.json_str)



### --- Данные по email адресам ---
class	UserEmailList():

    def	__init__(self):

	self.url = "%semail_list=" % url
	self.json_str = urllib2.urlopen(self.url).read()
	self.json_str = self.json_str.encode("utf-8")

	self.j = json.loads(self.json_str)




### --- Список пользователей ---
class	UserList():

    def	__init__(self):

	self.url = "%suser_list=" % url
	self.json_str = urllib2.urlopen(self.url).read()
	self.json_str = self.json_str.encode("utf-8")

	self.j = json.loads(self.json_str)



### --- Поступление данные в формате json ---
def	JsonService(request):

    response = HttpResponse("OK",content_type="text/plain")

    return response


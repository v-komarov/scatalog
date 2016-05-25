#coding:utf-8

import	datetime
from	django	import	forms
from	django.forms.extras.widgets	import	SelectDateWidget

from	scatalog.lib.userfiles	import	GetUserList

from	scatalog.lib.costcontract_report	import	GetContragentList

y = range(2000,2015)



block_list = [
    ['блок Магистраль','блок Магистраль'],
    ['блок Доступ','блок Доступ'],
    ['блок Эксплуатация','блок Эксплуатация'],
    ]

tema_list = [
    ['Аренда канала связи','Аренда канала связи'],
    ['Аренда кабельной канализации','Аренда кабельной канализации'],
    ['Аренда стойко-места','Аренда стойко-места'],
    ['Аренда ВОЛС','Аренда ВОЛС'],
    ['Подключение DSL РЖД','Подключение DSL РЖД'],
    ['Техническое обслуживание','Техническое обслуживание'],
    ['Прочее','Прочее'],
    ]

tema_list2 = [
    ['','BCE'],
    ['Аренда канала связи','Аренда канала связи'],
    ['Аренда кабельной канализации','Аренда кабельной канализации'],
    ['Аренда стойко-места','Аренда стойко-места'],
    ['Аренда ВОЛС','Аренда ВОЛС'],
    ['Подключение DSL РЖД','Подключение DSL РЖД'],
    ['Техническое обслуживание','Техническое обслуживание'],
    ['Прочее','Прочее'],
    ]



class	ContractForm(forms.Form):
    block = forms.ChoiceField(label='Блок *',choices=block_list)
    tema = forms.ChoiceField(label='Тема *',choices=tema_list)
    contragent = forms.CharField(label='Контрагент *')
    contract = forms.CharField(label='Номер договора *')
    file_load = forms.FileField(label='Файл ',widget=forms.FileInput,required=False)


### --- Поиск  ---
class	SearchForm(forms.Form):
    search = forms.CharField(label='Строка поиска',required=False)


class	OrderForm(forms.Form):
    order = forms.CharField(label='Номер заказа *')
    file_load = forms.FileField(label='Файл ',widget=forms.FileInput,required=False)
    cost = forms.DecimalField(label='Еж.м.платежи *',decimal_places=2)
    start_date = forms.DateField(label='Начало реализации *',widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    end_date = forms.DateField(label='Окончание реализации',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    clientorder = forms.CharField(label='Клиентский заказ',required=False)
    status = forms.ChoiceField(label='Статус *',choices=[['','---'],['Активный','Активный'],['Архивный','Архивный']])


## --- Отчет 1 ---
class	Report1Form(forms.Form):
    tema = forms.ChoiceField(label='Тема *',choices=tema_list2,required=False)
    contragent = forms.ChoiceField(label='Контрагент *',choices=[],required=False)
    def	__init__(self,*args,**kwargs):
	super(Report1Form,self).__init__(*args,**kwargs)
	c_list = []
	for item in GetContragentList():
	    c_list.append([item,item])
	c_list.insert(0,['','BCE'])
	self.fields['contragent'].choices = c_list



#coding:utf-8

import	datetime
from	django	import	forms
from	django.forms.extras.widgets	import	SelectDateWidget

from	scatalog.lib.userfiles	import	GetUserList


y = [2014,]


uselist = [
    ['',''],
    ['Стройка','Стройка'],
    ['Конфигурация ЦКС','Конфигурация ЦКС'],
    ['Прокладка UTP/ШПД','Прокладка UTP/ШПД'],
    ]

speedlist = [
    ['128 КБс','128 КБс'],
    ['256 КБс','256 КБс'],
    ['512 КБс','512 Кbs'],
    ['1 МБс','1 МБс'],
    ['2 МБс','2 МБс'],
    ['3 МБс','3 МБс'],
    ['4 МБс','4 МБс'],
    ['5 МБс','5 МБс'],
    ['6 МБс','6 МБс'],
    ['7 МБс','7 МБс'],
    ['8 МБс','8 МБс'],
    ['9 МБс','9 МБс'],
    ['10 МБс','10 МБс'],
    ['20 МБс','20 МБс'],
    ['30 МБс','30 МБс'],
    ['40 МБс','40 МБс'],
    ['50 МБс','50 МБс'],
    ['60 МБс','60 МБс'],
    ['70 МБс','70 МБс'],
    ['80 МБс','80 МБс'],
    ['90 МБс','90 МБс'],
    ['100 МБс','100 МБс'],
    ['1 ГБс','1 ГБс'],
    ]

### --- Тип услуги ---
typeservice = [
    ['Интернет (гарантия)','Интернет (гарантия)'],
    ['Интернет (ШПД)','Интернет (ШПД)'],
    ['IP VPN','IP VPN'],
    ['ЦКС','ЦКС'],
    ['Аренда ОВ','Аренда ОВ'],
    ['Аренда стойка-место','Аренда стойка-место'],
    ]


### --- Тип интерфейса ---
typeinterface = [
    ['G.703','G.703'],
    ['FastEthernet','FastEthernet'],
    ['GigabitEthernet','GigabitEthernet'],
    ['DSL','DSL'],
    ]

result = [
    ['На рассмотрении клиента','На рассмотрении клиента'],
    ['Согласовано с клиентом','Согласовано с клиентом'],
    ['Отказ клиента','Отказ клиента'],
    ]

statuslist = [
    ['Запрос','Запрос'],
    ['Принято в работу','Принято в работу'],
    ['Техническое решение','Техническое решение'],
    ['Коммерческая часть','Коммерческая часть'],
    ['Реализация','Реализация'],
    ['Принято в реализацию','Принято в реализацию'],
    ['Согласовано','Согласовано'],
    ]


priority_list = [
    ['Нормальный','Нормальный'],
    ['Срочно','Срочно'],
    ]


class	OrderForm(forms.Form):
    priority = forms.ChoiceField(label='Приоритет *',choices=priority_list)
    name = forms.CharField(label='Наименование *',widget=forms.TextInput(attrs={'class':'span7'}))
    address = forms.CharField(label='Адрес *',widget=forms.TextInput(attrs={'class':'span7'}))
    inn = forms.CharField(label='ИНН *')
    product = forms.ChoiceField(label='Продукт (РП,ЦП) *',choices=[['',''],['РП','РП'],['ЦП','ЦП']])
    point = forms.ChoiceField(label='Точность проработки *',choices=[['Бюджетная оценка','Бюджетная оценка'],['Детальная проработка','Детальная проработка']])
#    manager = forms.ChoiceField(label='Менеджер *',choices=[])

    service = forms.ChoiceField(label='Тип услуги *',choices=typeservice)
    speed = forms.ChoiceField(label='Скорость *',choices=speedlist)
    interface = forms.ChoiceField(label='Тип интерфейса *',choices=typeinterface)
    option = forms.CharField(label='Дополнительные требования',required=False,widget=forms.Textarea(attrs={'rows':4,'class':'span12'}))

    client = forms.CharField(label='Пред-ль клиента *')
    email = forms.EmailField(label='Email ',required=False)
    phone = forms.CharField(label='Телефон *')

#    def	__init__(self,*args,**kwargs):
#	super(OrderForm,self).__init__(*args,**kwargs)
#	userlist = GetUserList()
#	userlist.insert(0,['',''])
#	self.fields['manager'].choices = userlist



class	TechnicalForm(forms.Form):
    use = forms.ChoiceField(label='Способ реализации ',choices=uselist,required=False)
    onepay = forms.DecimalField(label='Разовый платеж ',decimal_places=2,widget=forms.TextInput(attrs={'class':'span4'}),required=False)
    monthpay = forms.DecimalField(label='Ежемесячный платеж ',decimal_places=2,required=False,widget=forms.TextInput(attrs={'class':'span4'}))
    option = forms.CharField(label='Дополнительные требования ',required=False)
    jobokp = forms.ChoiceField(label='ФИО сотрудника ОКП ',choices=[],required=False)
    nemis = forms.IntegerField(label='NeMis ',required=False,widget=forms.TextInput(attrs={'class':'span4'}))
    comment = forms.CharField(label='Комментарий ',required=False,widget=forms.Textarea(attrs={'rows':4,'class':'span12'}))
    def	__init__(self,*args,**kwargs):
	super(TechnicalForm,self).__init__(*args,**kwargs)
	userlist = GetUserList()
	userlist.insert(0,['',''])
	self.fields['jobokp'].choices = userlist



### ---
class	FileForm(forms.Form):
    file_link = forms.ChoiceField(label='Файл *',choices=[],required=False)



class	CommercialForm(forms.Form):
    kp = forms.DateField(label='Направлено КП *',widget=SelectDateWidget(years=y,attrs={'class':'span4'}),initial=datetime.date.today())
    onepay = forms.DecimalField(label='Разовый платеж *',decimal_places=2,widget=forms.TextInput(attrs={'class':'span4'}))
    monthpay = forms.DecimalField(label='Ежемесячный платеж *',decimal_places=2,widget=forms.TextInput(attrs={'class':'span4'}))
    manager = forms.ChoiceField(label='Менеджер *',choices=[])
    result = forms.ChoiceField(label='Результат *',choices=result)
    comment = forms.CharField(label='Комментарий ',required=False,widget=forms.Textarea(attrs={'rows':4,'class':'span12'}))

    def	__init__(self,*args,**kwargs):
	super(CommercialForm,self).__init__(*args,**kwargs)
	userlist = GetUserList()
	userlist.insert(0,['',''])
	self.fields['manager'].choices = userlist



class	RealBuildForm(forms.Form):
    smartasr_order = forms.IntegerField(label='Номер заказа СмартАСР ',required=False,widget=forms.TextInput(attrs={'class':'span4'}))
    date_order = forms.DateField(label='Дата подачи заказа ',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    date_tmc = forms.DateField(label='Дата заявки ТМЦ ',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    date_doc = forms.DateField(label='Дата передачи документации ',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    date_tmc_out = forms.DateField(label='Дата выдачи ТМЦ ',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    date_end = forms.DateField(label='Дата завершения строительства',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    sz = forms.CharField(label='Номер и дата оформления СЗ на реализацию в БЭ ',required=False,widget=forms.TextInput(attrs={'rows':4,'class':'span8'}))
    iss = forms.CharField(label='Номер и дата ИСС ',required=False,widget=forms.TextInput(attrs={'rows':4,'class':'span8'}))
    date_real = forms.DateField(label='Назначенная дата реализации',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    date_realend = forms.DateField(label='Дата завершения реализации',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    comment = forms.CharField(label='Комментарий ',required=False,widget=forms.Textarea(attrs={'rows':4,'class':'span12'}))



class	RealConfigForm(forms.Form):
    smartasr_order = forms.IntegerField(label='Номер заказа СмартАСР ',required=False,widget=forms.TextInput(attrs={'class':'span4'}))
    date_order = forms.DateField(label='Дата подачи заказа ',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    sz = forms.CharField(label='Номер и дата оформления СЗ на реализацию в БЭ ',required=False,widget=forms.TextInput(attrs={'rows':4,'class':'span8'}))
    date_real = forms.DateField(label='Назначенная дата реализации',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    date_realend = forms.DateField(label='Дата завершения реализации',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    comment = forms.CharField(label='Комментарий ',required=False,widget=forms.Textarea(attrs={'rows':4,'class':'span12'}))



class	RealUTPForm(forms.Form):
    smartasr_order = forms.IntegerField(label='Номер заказа СмартАСР ',required=False,widget=forms.TextInput(attrs={'class':'span4'}))
    date_order = forms.DateField(label='Дата подачи заказа ',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    iss = forms.CharField(label='Номер и дата ИСС ',required=False,widget=forms.TextInput(attrs={'rows':4,'class':'span8'}))
    date_real = forms.DateField(label='Назначенная дата реализации',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    date_realend = forms.DateField(label='Дата завершения реализации',required=False,widget=SelectDateWidget(years=y,attrs={'class':'span4'}))
    comment = forms.CharField(label='Комментарий ',required=False,widget=forms.Textarea(attrs={'rows':4,'class':'span12'}))



class	AddEmailForm(forms.Form):
    user = forms.ChoiceField(label='Пользователь *',choices=[])
    status = forms.ChoiceField(label='Статус *',choices=statuslist)

    def	__init__(self,*args,**kwargs):
	super(AddEmailForm,self).__init__(*args,**kwargs)
	userlist = GetUserList()
	userlist.insert(0,['',''])
	self.fields['user'].choices = userlist


### --- Поиск  ---
class	SearchForm(forms.Form):
    search = forms.CharField(label='Строка поиска',required=False)


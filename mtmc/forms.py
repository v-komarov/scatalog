#coding:utf-8

from	django	import	forms
from	scatalog.lib.mtmc	import	GetUserList





class	UserForm(forms.Form):
    user = forms.ChoiceField(label='По пользователю',choices=[],required=False)

    def	__init__(self,*args,**kwargs):
	super(UserForm,self).__init__(*args,**kwargs)
	userlist = GetUserList()
	userlist.insert(0,['ALL','BCE'])
	userlist.insert(0,['',''])
	self.fields['user'].choices = userlist



class	SearchForm(forms.Form):
    search = forms.CharField(label='По идентификатору')



class	MoveForm(forms.Form):
    user2 = forms.ChoiceField(label='Пользователь',choices=[],required=False)
    place = forms.CharField(label='Место',widget=forms.TextInput(attrs={'class':'span8'}))

    def	__init__(self,*args,**kwargs):
	super(MoveForm,self).__init__(*args,**kwargs)
	userlist = GetUserList()
	userlist.insert(0,['',''])
	self.fields['user2'].choices = userlist


class	NameForm(forms.Form):
    name = forms.CharField(label='Наименование *',widget=forms.TextInput(attrs={'class':'span8'}))


class	AttrForm(forms.Form):
    attr = forms.CharField(label='Атрибут *',widget=forms.TextInput(attrs={'class':'span2'}))
    value = forms.CharField(label='Значение *',widget=forms.TextInput(attrs={'class':'span5'}))


class	DataForm(forms.Form):
    d = forms.CharField(label='Компонент *',widget=forms.TextInput(attrs={'class':'span5'}))
    q = forms.IntegerField(label='Кол-во *',widget=forms.TextInput(attrs={'class':'span1'}))


class	StatusForm(forms.Form):
    status = forms.ChoiceField(label='Статус *',choices=[['',''],['Эксплуатация','Эксплуатация'],['Хранение','Хранение'],['Ремонт','Ремонт'],['Списан','Списан']])
    comment = forms.CharField(label='Комментарий ',widget=forms.TextInput(attrs={'class':'span5'}),required=False)


class	MForm(forms.Form):
    place = forms.CharField(label='Место',widget=forms.TextInput(attrs={'class':'span4'}),required=False)
    user = forms.ChoiceField(label='МОЛ *',choices=[])

    def	__init__(self,*args,**kwargs):
	super(MForm,self).__init__(*args,**kwargs)
	userlist = GetUserList()
	userlist.insert(0,['',''])
	self.fields['user'].choices = userlist


class	LoadFile(forms.Form):
    comment = forms.CharField(label='Комментарий ',widget=forms.TextInput(attrs={'class':'span5'}),required=False)
    file_load = forms.FileField(label='Файл*',widget=forms.FileInput,required=False)

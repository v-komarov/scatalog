#coding:utf-8

from	django	import	forms
from	scatalog.lib.userfiles	import	GetUserList


actionlist = (
['',''],
['begin','Начало'],
['continue','Продолжение'],
['end','Завершение'],
)


def	GetActionName(kod):
    for item in actionlist:
	if item[0] == kod:
	    return item[1]
    return '...'


class	SchemeForm(forms.Form):
    name = forms.CharField(label='Название схемы *')


class	StepForm(forms.Form):
    step_number = forms.IntegerField(label='Номер шага *',widget=forms.TextInput(attrs={'class':'span2'}))
    step_name = forms.CharField(label='Название шага *')
    user = forms.ChoiceField(label='Исполнитель *',choices=GetUserList())
    action = forms.ChoiceField(label='Действие *',choices=actionlist)
    step_yes = forms.IntegerField(label='Да к шагу *',widget=forms.TextInput(attrs={'class':'span2'}))
    step_no = forms.IntegerField(label='Нет к шагу *',widget=forms.TextInput(attrs={'class':'span2'}))
    function = forms.CharField(label='Функция ',required=False)

    def	__init__(self,*args,**kwargs):
	super(StepForm,self).__init__(*args,**kwargs)
	userlist = GetUserList()
	userlist.insert(0,['',''])
	self.fields['user'].choices = userlist


class	AttrForm(forms.Form):
    name = forms.CharField(label='Название атрибута *')


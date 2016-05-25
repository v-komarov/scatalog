#coding:utf-8

from	django	import	forms
from	scatalog.lib.proc	import	GetSchemeList,ListFileAll,GetAttrsAll



statuslist = (
    ('Подготовка','Подготовка'),
    ('Выполняется','Выполняется'),
    ('Остановлен','Остановлен'),
    ('Завершен','Завершен'),
)



class	ProcForm(forms.Form):
    name = forms.CharField(label='Название процесса *')
    scheme = forms.ChoiceField(label='Схема *',choices=[])
    status = forms.ChoiceField(label='Статус *',choices=statuslist)
    info = forms.CharField(label='Описание',widget=forms.Textarea(attrs={'cols':15,'rows':5,'class':'span10'}),required=False)

    def	__init__(self,*args,**kwargs):
	super(ProcForm,self).__init__(*args,**kwargs)
	userlist = GetSchemeList()
	userlist.insert(0,['',''])
	self.fields['scheme'].choices = userlist



class	CommentForm(forms.Form):
    comment = forms.CharField(label='Комментарий',widget=forms.Textarea(attrs={'cols':15,'rows':5,'class':'span10'}),required=False)
    file_link = forms.ChoiceField(label='Файл',choices=[],required=False)

    def	__init__(self,*args,**kwargs):
	super(CommentForm,self).__init__(*args,**kwargs)
	filelink = ListFileAll()
	self.fields['file_link'].choices = filelink


class	StepForm(forms.Form):
    yesno = forms.ChoiceField(label='Решение *',choices=[['yes','Согласовать'],['no','Отклонить']])
    comment = forms.CharField(label='Комментарий',required=False,widget=forms.TextInput(attrs={'class':'span6'}))



class	AttrForm(forms.Form):
    attr = forms.ChoiceField(label='Атрибут *',choices=[])
    value = forms.CharField(label='Значение *',widget=forms.TextInput(attrs={'class':'span5'}))

    def	__init__(self,*args,**kwargs):
	super(AttrForm,self).__init__(*args,**kwargs)
	attrs = GetAttrsAll()
	self.fields['attr'].choices = attrs


#coding:utf-8

from	django	import	forms
from	scatalog.lib.userfiles	import	GetEmailList,GetUserList



class	LoadFile(forms.Form):
    comment = forms.CharField(label='Описание файла',widget=forms.Textarea(attrs={'cols':15,'rows':5,'class':'span8'}),required=False)
    file_load = forms.FileField(label='Файл*',widget=forms.FileInput,required=False)



class	SendLinkFile(forms.Form):
    comment = forms.CharField(label='Комментарий',widget=forms.Textarea(attrs={'cols':15,'rows':5,'class':'span8'}),required=False)
    user = forms.ChoiceField(label='Адресат *',choices=GetEmailList())

    def	__init__(self,*args,**kwargs):
	super(SendLinkFile,self).__init__(*args,**kwargs)
	emaillist = GetEmailList()
	emaillist.insert(0,['',''])
	self.fields['user'].choices = emaillist



### --- Поиск  ---
class	SearchForm(forms.Form):
    search = forms.CharField(label='Строка поиска',required=False)



class	AccessType(forms.Form):
    access = forms.ChoiceField(label='Вид доступа *',choices=[['private','private'],['user','user'],['public','public']])



class	AccessUser(forms.Form):
    user = forms.ChoiceField(label='Пользователь *',choices=GetUserList())

    def	__init__(self,*args,**kwargs):
	super(AccessUser,self).__init__(*args,**kwargs)
	userlist = GetUserList()
	userlist.insert(0,['',''])
	self.fields['user'].choices = userlist


class	EditComment(forms.Form):
    comment = forms.CharField(label='Описание файла',widget=forms.Textarea(attrs={'cols':15,'rows':5,'class':'span8'}))


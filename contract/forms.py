#coding:utf-8

from	django	import	forms

### --- Поиск  ---
class	SearchForm(forms.Form):
    search = forms.CharField(label='Строка поиска',required=False)


### --- Загрузка договора ---
class	LoadContract(forms.Form):
    contragent = forms.CharField(label='Контрагент *')
    comment = forms.CharField(label='Комментарий *')
    file_load = forms.FileField(label='Файл*',widget=forms.FileInput,required=False)


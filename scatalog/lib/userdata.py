#coding:utf-8



def	GetFio(request):

    fio = request.session['key777'][0].split('#')[5]
    a = fio.split('|')
    fio = a[0]+' '+a[1]+' '+a[2]

    return fio
    
    
def	GetPhone(request):

    phone = request.session['key777'][0].split('#')[5]
    a = phone.split('|')
    phone = a[3]
    
    return phone


def	GetEmail(request):

    email = request.session['key777'][0].split('#')[5]
    a = email.split('|')
    email = a[4]

    return email


def	GetUserKod(request):
    kod = request.session['key777'][0].split('#')[0]
    return kod



def	CheckAccess(request,mod_kod):
    
    access_str = request.session['key777'][0].split('#')[3]
    access = access_str.split(':')

    try:
        access.index(mod_kod)
        return 'OK'
    except:
        return 'NOTACCESS'



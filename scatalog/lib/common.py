#coding:utf-8



def	Compare(frase,word):
    
    frase = frase.lower().encode('utf-8')
    word = word.lower().encode('utf-8')

    if frase.find(word)!=-1:
	return True
    else:
	return False


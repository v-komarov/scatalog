#coding:utf-8


from	django.http	import	HttpResponse
from	django.http	import	HttpResponseRedirect
from	django.template	import	Context, loader, RequestContext
from	django.core.context_processors	import	csrf
from	django.shortcuts	import	render_to_response

from	reportlab.pdfgen	import	canvas
from	reportlab.lib.units	import	mm
from	reportlab.pdfbase	import	pdfmetrics
from	reportlab.pdfbase	import	ttfonts
from	reportlab.lib		import	colors
from	reportlab.lib.pagesizes	import	letter, A4, landscape

from	reportlab.platypus.tables	import	Table, TableStyle
from	reportlab.platypus.doctemplate	import	SimpleDocTemplate
from	reportlab.platypus.paragraph	import	Paragraph
from	reportlab.lib.styles		import	ParagraphStyle,getSampleStyleSheet
from	reportlab.platypus		import	Frame,Spacer

from	reportlab.platypus		import	Image


from	mtmc				import	GetList



### --- Печатная форма кодов ---
def	PrintForm(buff,user_id):

    #### --- Получение списка ---
    eq_list = GetList(user_id)


    Font1 = ttfonts.TTFont('PT','scatalog/fonts/PTC55F.ttf')
    Font2 = ttfonts.TTFont('PTB','scatalog/fonts/PTC75F.ttf')
    Font3 = ttfonts.TTFont('PTI','scatalog/fonts/PTS56F.ttf')


    pdfmetrics.registerFont(Font1)
    pdfmetrics.registerFont(Font2)
    pdfmetrics.registerFont(Font3)


    style = getSampleStyleSheet()
    style.add(ParagraphStyle(name='MyStyle',wordWrap=True,fontName='PTB',fontSize=10,spaceAfter=5*mm,spaceBefore=20*mm,alignment=0))
    style.add(ParagraphStyle(name='MyStyle0',wordWrap=True,fontName='PT',fontSize=10,spaceAfter=5*mm,spaceBefore=5*mm,alignment=0))
    style.add(ParagraphStyle(name='MyStyle2',wordWrap=True,fontName='PT',fontSize=8,spaceAfter=1*mm,spaceBefore=1*mm,alignment=1))
    
    doc = SimpleDocTemplate(buff,topMargin=10*mm,bottomMargin=10*mm,leftMargin=20*mm,rightMargin=10*mm)

    tail = len(eq_list)%5
    eq_tail = eq_list[-tail:]

    data = []
    i = []
    t = []
    for row in eq_list:
	if len(i) != 5:
	    I = Image('scatalog/static/img/qrcode/%s.png' % row[0])
	    I.drawHeight = 20*mm
	    I.drawWidth = 20*mm
	    i.append(I)
	    t.append(Paragraph(row[1],style["MyStyle2"]))
	else:
	    data.append(i)
	    data.append(t)
	    i = []
	    t = []



    i = []
    t = []
    for row in eq_tail:
	I = Image('scatalog/static/img/qrcode/%s.png' % row[0])
	I.drawHeight = 20*mm
	I.drawWidth = 20*mm
	i.append(I)
	t.append(Paragraph(row[1],style["MyStyle2"]))
    data.append(i)
    data.append(t)
	



    t=Table(data)
    t.setStyle([('FONTNAME',(0,0),(-1,-1),'PTB'),
		('FONTSIZE',(0,0),(-1,-1),10),
		('ALIGN',(0,0),(-1,-1),'CENTER'),
		('VALIGN',(0,0),(-1,-1),'MIDDLE'),
		('GRID',(0,0),(-1,-1),0.25,colors.black),
		])


    elements = []
    

    elements.append(t)
    
    doc.build(elements)

    return buff

from	django.conf.urls	import	patterns, include, url
from	django.contrib.staticfiles.urls	import	staticfiles_urlpatterns
from	django.conf	import	settings


#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scatalog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'start.views.Home'),
    url(r'^exit/$', 'start.views.Exit'),


    url(r'^userfiles/$', 'userfiles.views.List'),
    url(r'^userfilenew/$', 'userfiles.views.New'),
    url(r'^getfile/$', 'userfiles.views.GetFile'),
    url(r'^sendfilelink/$', 'userfiles.views.SendFile'),
    url(r'^userfileaccess/$', 'userfiles.views.AccessFile'),
    url(r'^otherfiles/$', 'userfiles.views.OtherFiles'),
    url(r'^userfileedit/$', 'userfiles.views.Edit'),


    url(r'^proc/$', 'proc.views.ProcList'),
    url(r'^procdata/$', 'proc.views.ProcData'),
    url(r'^procstep/$', 'proc.views.ProcStep'),
    url(r'^proccomment/$', 'proc.views.ProcComment'),
    url(r'^procemail/$', 'proc.views.ProcEmail'),
    url(r'^procfiles/$', 'proc.views.ProcFiles'),
    url(r'^procattrs/$', 'proc.views.ProcAttrs'),
    url(r'^scheme/$', 'scheme.views.SchemeList'),
    url(r'^schemenew/$', 'scheme.views.SchemeNew'),
    url(r'^schemeedit/$', 'scheme.views.SchemeEdit'),
    url(r'^schemeattrs/$', 'scheme.views.SchemeAttrs'),

    url(r'^contract/$', 'contract.views.ContractList'),
    url(r'^contractnew/$', 'contract.views.ContractNew'),


    url(r'^mtmc/$', 'mtmc.views.List'),
    url(r'^mtmcnew/$', 'mtmc.views.New'),
    url(r'^mtmcedit/$', 'mtmc.views.Edit'),
    url(r'^mtmcattrs/$', 'mtmc.views.Attrs'),
    url(r'^mtmcdata/$', 'mtmc.views.Data'),
    url(r'^mtmcstatus/$', 'mtmc.views.Status'),
    url(r'^mtmcmove/$', 'mtmc.views.Move'),
    url(r'^mtmcfiles/$', 'mtmc.views.Files'),


    url(r'^clientlist/$', 'client.views.List'),
    url(r'^clientnew/$', 'client.views.New'),
    url(r'^client/$', 'client.views.Client'),
    url(r'^technical/$', 'client.views.Technical'),
    url(r'^commercial/$', 'client.views.Commercial'),
    url(r'^realization/$', 'client.views.Real'),
    url(r'^realbuild/$', 'client.realization.RealBuild'),
    url(r'^realconfig/$', 'client.realization.RealConfig'),
    url(r'^realutp/$', 'client.realization.RealUTP'),
    url(r'^clientstatus/$', 'client.views.StatusList'),
    url(r'^clientemail/$', 'client.views.EmailList'),
    url(r'^clientopt/$', 'client.options.Options'),
    url(r'^clientrep/$', 'client.reports.Reports'),


    url(r'^costcontract/$', 'costcontract.views.List'),
    url(r'^costcontractnew/$', 'costcontract.views.New'),
    url(r'^costcontractedit/$', 'costcontract.views.Edit'),
    url(r'^costcontractfile/$', 'costcontract.views.File'),
    url(r'^costcontractorder/$', 'costcontract.views.Order'),
    url(r'^costcontractordernew/$', 'costcontract.views.NewOrder'),
    url(r'^costcontractorderedit/$', 'costcontract.views.EditOrder'),
    url(r'^costcontractreport/$', 'costcontract.views.Report'),



    url(r'css/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/coca/scatalog/scatalog/static/css/',}),
    url(r'js/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/coca/scatalog/scatalog/static/js/',}),
    url(r'img/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/coca/scatalog/scatalog/static/img/',}),

)

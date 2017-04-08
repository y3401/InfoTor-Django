from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Torrents, Category, Forum, Contents, Vers
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from zlib import decompress
import infotor.modbbcode as bbc
from django.db.models import Q
from django.core.paginator import Paginator,InvalidPage
import re
from django.db import connections

def outlist(i,p_num):
    shtml=''' <a href="#" onclick="setpar('poz',{});">[ {} ] </a>'''
    if i!=int(p_num):
        pg = shtml.format(str(i),str(i))
    else:
        pg = '<b>[ %s ]</b> ' % str(i)
    return pg        

def squery(fraze='',razdel='0',frm='0'):
    sfq='''SELECT name_category, name_forum, file_id, hash_info, title, size_b, date_reg, code_forum 
    FROM (torrent AS t inner join forum AS f on t.forum_id=f.code_forum) 
    inner join category AS C on f.category_id=C.code_category WHERE size_b>0 '''
    sfq+=splitter(fraze)
    if razdel!='00':
        sfq+=' AND f.category_id=%s ' % (str(int(razdel)),)
    if frm!='0':
        sfq+=' AND f.code_forum=%s ' % (str(int(frm)),)
    sfq+=' ORDER BY f.category_id asc, f.name_forum asc, file_id desc'
    return sfq

def splitter(text=''):
    ssq=''
    for fraza in re.findall(r"[\'\"](.*?)[\'\"]",text):
        text=text.replace(fraza,'')
        if len(fraza)>0: ssq+=' AND lower(title) LIKE "%'+fraza.lower()+'%"'
    for word in re.split(r'\s',text):
        word=re.sub(r'[\"\'\*\+\<\>?]','',word)
        if len(word)>0: ssq+=' AND (lower(title) LIKE "%'+word.lower()+'%" OR title LIKE "%'+word.capitalize()+'%")'
    return ssq

def search(request):
    template_name = 'infotor/search.html'
    result_cat = Category.objects.order_by('code_category')
    vers = Vers.objects.get(pk=1)
    version = 'Версия базы от %s.%s.%s' % (str(vers)[-2:],str(vers)[4:6],str(vers)[:4])
    razd = request.GET.get('category',default='00')
    podr = request.GET.get('podr',default='0')
    querytext = request.GET.get('querytext',default='')
    page_num = request.GET.get('page',default='1')
            
    if querytext!='' or podr!='0':
        mode=1
        sql=squery(querytext,razd,podr)
        paginator = Paginator((list(Torrents.objects.raw(sql))),100)
        countrec = str(paginator.count)
    elif razd!='00':
        mode=2
        paginator=Paginator(Forum.objects.filter(category_id=razd).order_by("name_forum"),200)
        countrec = str(paginator.count)
    elif querytext=='' and razd=='00':
        mode=0
        paginator=Paginator(Torrents.objects.order_by("file_id"),1)
        countrec = str(paginator.count)
    
    if countrec[-1:] == '1' and countrec != '11':
        zap=' запись'
    elif countrec in ('11','12','13','14') or countrec[-1:] in ('0','5','6','7','8','9'):
        zap=' записей'
    else:
        zap=' записи' 
    if page_num=='':
        page_num='1'
    
    pager=''
    if int(countrec)>0:
        smax=((int(countrec)-1)//100)+1
        L = range(0,smax)
        pcur=int(page_num)
        pmin = pcur - 4
        pmax = pcur + 5
        if pmin < 2: 
            pmin = 2
        if pmax > smax: 
            pmax = smax
        pager += outlist(1,page_num)
        if pcur>6: 
            pager += ' ... '
        for j in L[pmin:pmax]:
            pager += outlist(j,page_num)
        if pcur < smax-5: 
            pager += ' ... '
        if smax!=1: 
            pager += outlist(smax,page_num)
    
    return render(request, template_name, {
        "category": result_cat,
        "sel_category": int(razd), 
        "forum":podr,
        "vers":version,
        "querytext":querytext,
        "result":paginator.page(page_num),
        "pozlist":(int(page_num)-1)*100,
        "countrec":countrec+zap,
        "mode":mode,
        "pager":pager,
       })

def info(request,file_id):
    template_name = 'infotor/info.html'
    try:
        result=Torrents.objects.all().get(pk=file_id)
    except (KeyError, Torrents.DoesNotExist):
        result=None

    try:
        cont=Contents.objects.get(tid=file_id)       
        if cont:
            S=decompress(cont.cont)
            result2 = bbc.bbcode2html(S.decode('utf-8'))

    except (KeyError, Contents.DoesNotExist):
        result2 = ":("

    return render(request, template_name, {"result": result,"result2": result2})


#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

########################################
# elji order.se Data Fetcher           #
# patterns.py, Regular expresions etc. #
# copyleft 2009, tofu3 softworks       #
########################################

import re
from libtofu import *
import string

reAN  = re.compile('width="50"><a href="article\.asp\?ArticleNo=([^&]*)&')
reImg = re.compile('<img src="([^"]*)"')
reNam = re.compile('<h3>(.*?)</h3>')
reEAN = re.compile('<td align="left"><b>EAN: ([0-9]*?)</b></td>')
reDsc = re.compile('<td colspan="3"><b>Beskrivning</b>(.*?)</td>', re.DOTALL)
reSpc = re.compile('<b>Specifikationer</b><br><br>(.*?)<br><br>')
reExt = re.compile('Ditt pris: <span class="articlecustomerprice">([0-9]*.?[0-9]*,[0-9]*) SEK</span></td>\s*</tr>\s*<tr>\s*<td>&nbsp;</td>\s*</tr>\s*<tr>\s*<td align="left">Lagersaldo: ([0-9]+)</td>\s*</tr>\s*<tr>\s*<td align="left">([^<]*)</td>')
reDCL = re.compile('(.*)<span name="expandDescText" id="expandDescText" style="display: none">(.*)\s*</span><a id="moreDescText" href="javascript:toggleDescText\(\)">\s*Visa mer...</a>\s*')
    
def anparse(a,ol = 0):
    ares = httpget('http://www.order.se/article.asp?ArticleNo=%s' % a)
    #sa = a
    #transtable = string.maketrans("/","_")
    #sa.translate(transtable) 
    #f = file('test/%s.txt' % sa,'w')
    #f.write(ares)
    #f.close()
    arr = strparse(ares)
    #return "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % strparse(ares)
    
    if arr['Name']:
        if arr['Desc'] and ol:
            arr['Desc'] = stripmultispaces(removebadchars(cleandesc(arr['Desc'],'<!--more-->')))
        else:
            arr['Desc'] = ''
        return arr
    else:
        return None

def cleandesc(s,sep = ''):
    m = reDCL.search(s)
    if m:
        o = m.group(1) + sep + m.group(2)
    else: o = s
    return o

def removebadchars(s):
    s = re.sub('["\n\r]', '', s)
    s = re.sub('&nbsp;', '', s)
    s = re.sub('\t', ' ', s)
    return s
    
def stripmultispaces(s):
    lastspace = False
    o = ''
    for c in s:
        if c == ' ':
            if not lastspace:
                o += c
                lastspace = True
        else:
            o += c
            lastspace = False
    return o
            
def cleanprice(s):
    o = ''
    for c in s:
        if c in '0123456789,':
            o += c
    return o
   
def strparse(s):
    a = 0
    ii = ''
    
    try: img = reImg.search(s).group(1)
    except: img = ii
    try: nam = removebadchars(reNam.search(s).group(1))
    except: nam = ii
    try: ean = reEAN.search(s).group(1)
    except: ean = ii
    try: dsc = reDsc.search(s).group(1) # RemoveBadChars moved to ANParse
    except: dsc = ii
    try: spc = removebadchars(reSpc.search(s).group(1))
    except: spc = ii
    try:
        mExt = reExt.search(s)
        prc = cleanprice(mExt.group(1))
        stk = mExt.group(2)
        dtm = mExt.group(3)
    except:
        prc = ii
        stk = ii
        dtm = ii
    
    oan = a
    fab = ii
    pr2 = ii
    return {'OwnArtNum':oan, 'Name':nam, 'ArtNum':a, 'Price':prc, 'Price2':pr2, 'EAN':ean, 'Image':img, 'Desc':dsc, 'Spec':spc, 'Stock':stk, 'DTM':dtm}

# Not needed, kept in case of later use:
'''
def saparse(i):
    sres = httpget('http://www.order.se/searchbyarticle.asp?Sort=0&SortOrder=0&mode=searcharticle&searchType=0&SearchPhrase=&Page=%d' % i)
    m = reAN.findall(sres)
    return m
'''

if __name__ == '__main__':
    
    f = open('test_input.txt','r')
    html = f.read()
    out = strparse(html)
    for ident,val in out.items():
        if ident == 'Desc':
            val = cleandesc(val,'\nDescFort: ')
        print '%s: %s' % (ident,val)
    
    #print stripmultispaces('lala    lalalala  fniz fniz kaka   ka     ka ka    ka ka')
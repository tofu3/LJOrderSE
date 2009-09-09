#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

###################################
# elji order.se Data Fetcher      #
# ljorderse.py, Main script       #
# copyleft 2009, tofu3 softworks  #
###################################

import sys,re,urllib,os,urllib2

# Replaced by os.system(title)
#import win32api

from patterns import *
from libt3httpget import *
import ConfigParser
from string import Template

confFile = 'ljorderse.conf'

ollist = ['limited','full']

# Short function: Print to stdout without spaces or newlines
def _(s):
    sys.stdout.write(s)

# Short function: Write to specified file (append mode)   
def _f(s,f):
    h = open(f, 'a')
    r = h.write(s)
    h.close()
    return r

# Read a database file, get article numbers (first column)
def getartnos(dbdump):
    out = []
    f = file(dbdump,'r')
    drl = ''
    for line in f.readlines():
        drl = line.split(';')
        out.append(drl[0])
    return out
    
# Log in to order.se with provided credentials
def auth(n,u,p):
    global opener
    params = urllib.urlencode(dict(CustomerNo=n, UserName=u, UserPassword=p, action='login', gui=1))
    f = opener.open('http://www.order.se/logindo.asp', params)
    data = f.read()
    f.close()
    return data
    
# Format data list as a CSV-type string
def dataformat(arr,ano):
    #Artikelnr;Benämning;Fabrikat;Tillverk.art.nr.;Pris;PrismMoms;EAN;Bild;Beskrivning;Specifikation;LagerSaldo;LevTid
    syntax = Template('$OwnArtNum;$Name;;$ArtNum;$Price;$Price2;$EAN;$Image;$Desc;$Spec;$Stock;$DTM\n')
    arr['OwnArtNum'] = ano
    arr['ArtNum'] = ano
    return syntax.safe_substitute(arr)

# Main function
if __name__ == "__main__":
    x = chr(int('B0', 16))
    y = chr(int('B1', 16))
    z = chr(int('B2', 16))
    os.system('title elji order.se Data Fetcher')
    print '\n '+x+y+z+'   elji order.se Data Fetcher   '+z+y+x+'\n '+x+y+z+' copyleft 2009, tofu3 softworks '+z+y+x+'\n'
    outlevel = 0
    if len(sys.argv)>1:
        if sys.argv[1] == '--full' or sys.argv[1] == '-f':
            outlevel = 1
        else:
            print ' Usage: ljorderse [-f|--full]\n -f or --full   Fetch all data, including description.\n'
            raw_input(' Press any key to quit...')
            sys.exit()
    print ' Output level: %s.' % ollist[outlevel]
    print ' Reading settings...',
    config = ConfigParser.RawConfigParser()
    config.read(confFile)
    OUT = config.get('settings','outputdatafile')
    INP = config.get('settings','inputdatafile')
    CustNo = config.get('authentication','CustomerNumber')
    User = config.get('authentication','Username')
    Pass = config.get('authentication','Password')
    PassMask = ''
    for i in range(0,len(Pass)):
        PassMask += '*'
    print 'OK'
    print ' Reading input data file...',
    if not os.path.isfile(INP):
        print "Error!\n\n Input data file does not exist. Please edit the configuration file.\n"
        raw_input(' Press any key to quit...')
        sys.exit()
    print " "
    artnos = getartnos(INP)
    print '  + Got %d entries.' % len(artnos)
    if CustNo and User and Pass:
        print ' Logging in with: #:%s U:%s P:%s...' % (CustNo,User,PassMask),
        auth(CustNo,User,Pass)
        print "OK"
        print ' + Cookies:'
        for cookie in jar:
            print '    + %s: %s' % (cookie.name,cookie.value)
    else:
        print ' No authentication information in config file. Skipping...'
        print ' /!\\ Warning /!\\ Cannot get all data without logging in.'
    print ' Writing output header...',
    try: os.remove(OUT)
    except: pass
    _f(u'Artikelnr;Benämning;Fabrikat;Tillverk.art.nr.;Pris;PrismMoms;EAN;Bild;Beskrivning;Specifikation;LagerSaldo;LevTid\n'.encode('latin-1'),OUT)
    print 'OK'
    print ' Requesting and parsing datasheets...'
    failedans = []
    for an in artnos:
        an = an.strip()
        try:
            i = int(an)
        except ValueError:
            i = 0
        if 1>0:
            print '  + Processing %s...' % an,
            andata = anparse(an,outlevel)
            if andata:
                _f(dataformat(andata,an),OUT)
                #print 'P:%s' % andata['Price'],
                print 'OK'
            else:
                print 'Fail!'
                failedans.append(an)
    print '\n All done! New data is saved to "%s".' % OUT
    if len(failedans):
        strfails = 'FAILURE LOG\n¯¯¯¯¯¯¯¯¯¯¯\n'
        for anf in failedans:
            strfails += 'Could not fetch data from http://www.order.se/article.asp?ArticleNo=%s\n' % anf
        f = file('faillog.txt','w')
        f.write(strfails)
        f.close()
        print ' \n/!\\ Some articles could not be fetched. Check faillog.txt for details.'
    raw_input('\n Press any key to continue...')

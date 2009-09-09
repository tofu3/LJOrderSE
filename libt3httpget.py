#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

###################################
# tofu3 httplib                   #
# copyleft 2009, tofu3 softworks  #
###################################

import urllib2, cookielib

jar = cookielib.MozillaCookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
urllib2.install_opener(opener)

def httpget(u):
    global opener
    f = opener.open(u)
    s = f.read()
    f.close()
    return s
#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

##################################
# tofu3 build_installer          #
#                   (winrar SFX) #
# copyleft 2009, tofu3 softworks #
##################################

import shutil,os,sys
from string import Template
from datetime import date
import subprocess as sp

# BEGIN Configuration --------------------------------

template = 'ljorderse-installer-template'

# Valid variables: build, date
output = Template('ljorderse-installer-$date-$build.exe')

rarpath = 'c:/Program files/WinRAR/rar.exe'

# END Configuration ----------------------------------

if __name__ == '__main__':
    f = open('rel/lastbuild.txt','r')
    old_build = f.read()
    f.close()
    new_build = int(old_build) + 1
    print ' Last build was: ' + old_build
    print ' Packaging build %d...' % new_build
    print ' - Copying template...',
    build_date = date.today().strftime("%y%m%d")
    outfile = output.safe_substitute({'date': build_date, 'build': new_build})
    shutil.copy('rel/'+template,'rel/'+outfile)
    print 'OK'
    print ' - Adding files to installer...',
    cmdout = sp.Popen([rarpath,'u','-idq','-ep1','rel/'+outfile,'dist/*'], stdout=sp.PIPE).communicate()[0]
    if cmdout != '':
        print 'Error!'
        print cmdout
        sys.exit(2)
    print 'OK'
    print ' - Writing new state files...',
    f = open('rel/lastbuild.txt','w')
    f.write(str(new_build))
    f.close()
    f = open('rel/lastrelease.txt','w')
    f.write(outfile)
    f.close()
    print 'OK'
    print '\n All done!'
    
    
    
from distutils.core import setup
import py2exe, sys, os,shutil

#sys.argv.append('py2exe')

try:
    shutil.rmtree('dist')
except: pass
shutil.copytree('dist_add','dist')

setup(
    options = {'py2exe': {'optimize': 2, 'bundle_files': 1}},
    console = [{
        'script': "ljorderse.py",
        "icon_resources": [(0, "res/t3.ico")]
        }],
    zipfile = None,
)

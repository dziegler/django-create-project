#!/usr/bin/env python
from django.core import management
import sys
import os
import create_project
import shutil
import re

def copy_files(root_path):
    base_dir = os.path.join(os.path.dirname(create_project.__file__),'files')
    for file in os.listdir(base_dir):
        if not file.startswith('.') and not file.endswith('.pyc'):
            shutil.copyfile(os.path.join(base_dir,file),os.path.join(root_path,file))

def update_settings(root_path):
    settings_file = os.path.join(root_path, 'settings.py')
    settings = open(settings_file, 'r').read().split('\n')
    
    # add project path
    settings.insert(1,os.linesep+"import os"+os.linesep+"PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])")
    
    # add template context processors
    idx = settings.index('MIDDLEWARE_CLASSES = (') -1
    settings.insert(idx,os.linesep+"""TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)"""+os.linesep)
    
    idx = settings.index('TEMPLATE_DIRS = (')
    del settings[idx+1:idx+5]
    
    # update middleware
    idx = settings.index('MIDDLEWARE_CLASSES = (')
    settings.insert(idx+4,"    'debug_toolbar.middleware.DebugToolbarMiddleware',")
    
    # remove installed apps
    idx = settings.index('INSTALLED_APPS = (')
    del settings[idx:idx+5]
    
    settings = os.linesep.join(settings)
    
    # set debug = False
    settings = re.sub(r"(?<=DEBUG) = True"," = False",settings)
    
    # set media paths
    settings = re.sub(r"(?<=MEDIA_ROOT) = ''"," = os.path.join(PROJECT_PATH,'static')",settings)
    settings = re.sub(r"(?<=MEDIA_URL) = ''"," = '/static/'",settings)
    
    # set time zone
    settings = re.sub(r"(?<=TIME_ZONE) = 'America/Chicago'"," = 'America/Los_Angeles'",settings)
    
    # set template dir
    settings = re.sub(r"(?<=TEMPLATE_DIRS) = \(",""" = (
    os.path.join(PROJECT_PATH, 'templates')""",settings)
    
    # add installed apps and settings
    settings += """

INSTALLED_APPS = (
    # included
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    
    # external
    'compressor',
    'django_extensions',
    'debug_toolbar',
)    

# cache settings
# ./memcached -d -m 5 -l 127.0.0.1 -p 18598
CACHE_SECONDS = 2000000
CACHE_BACKEND = 'memcached://127.0.0.1:18598/?timeout='+str(CACHE_SECONDS)

# debug toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

# django_css
COMPILER_FORMATS = {
    '.ccss': {
        'binary_path':'clevercss',
        'arguments': '*.ccss'
    },
}
COMPRESS_YUI_BINARY = os.path.join('java -jar '+PROJECT_PATH,'yuicompressor-2.4.2.jar')
COMPRESS_CSS_FILTERS = ('compressor.filters.yui.YUICSSFilter',)
COMPRESS_JS_FILTERS = ('compressor.filters.yui.YUIJSFilter',)

try:    
    from localsettings import *
except:
    pass
"""
    file = open(settings_file, 'w')
    file.write(settings)
    file.close()
    
def main():
    # command line hack
    sys.argv.append(sys.argv[1])
    sys.argv[1] = 'startproject'
    management.execute_from_command_line()
    
    root_path = os.path.join(os.getcwd(),sys.argv[2])
    for dir in ('apps','scripts','static','templates'):
        os.mkdir(os.path.join(root_path,dir))
        if dir == 'scripts':
            file = open(os.path.join(root_path,dir,'__init__.py'),'w')
            file.close()
        if dir == 'static':
            [os.mkdir(os.path.join(root_path,dir,static_dir)) for static_dir in ('css','js','images')]
    copy_files(root_path)
    update_settings(root_path)

if __name__ == "__main__":
    main()
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'portal.settings'

from portal.wsgi import application

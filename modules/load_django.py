import os
import sys
import django


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)


os.environ['DJANGO_SETTINGS_MODULE'] = 'braincomua_playwright_project.settings'

django.setup()
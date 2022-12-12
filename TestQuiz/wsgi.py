"""
WSGI config for TestQuiz project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.path.isfile(os.path.join(os.path.dirname(__file__), 'settings_local.py')):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestQuiz.settings_local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestQuiz.settings')



application = get_wsgi_application()

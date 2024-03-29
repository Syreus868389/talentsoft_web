"""
WSGI config for talentsoft_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

env('DJANGO_SETTINGS_MODULE')

application = get_wsgi_application()

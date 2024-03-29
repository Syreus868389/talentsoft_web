"""
ASGI config for talentsoft_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

env('DJANGO_SETTINGS_MODULE')

application = get_asgi_application()

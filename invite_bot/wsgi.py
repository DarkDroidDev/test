"""
WSGI config for invite_bot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from telegram import Bot

from .config import BOT_KEY

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invite_bot.settings')

application = get_wsgi_application()

bot = Bot(BOT_KEY)
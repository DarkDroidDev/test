from django.urls import path
from .views import setWebHook,deleteWebHook, response

app_name = 'bot'

urlpatterns = [
	path('setwebhook/', setWebHook, name='setwebhook'),
	path('deletewebhook/', deleteWebHook, name='deletewebhook'),
	path('response/', response),
]
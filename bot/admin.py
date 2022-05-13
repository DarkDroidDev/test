from django.contrib import admin
from django.utils.html import format_html

from telegram.utils.helpers import mention_html

from .models import User, Translation
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('name', 'referrees', 'status','note', 'overflow', 'link', 'referral_link')
	readonly_fields = ('name', 'referrees', 'status', 'overflow', 'link', 'referral_link', 'id')
		
		
@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
	list_display = ('lookup', 'lang','translated_text',)
	


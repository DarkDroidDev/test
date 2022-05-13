from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
from invite_bot.wsgi import bot
from invite_bot.config import WEBHOOK_URL, BOT_KEY, ADMIN_ID, MAX_INVITE

from telegram import (
	Update,
	Chat,
	ParseMode
)

import json
from django.views.decorators.csrf import csrf_exempt

from .command import start, detail, commands
from .utils import extract_status_change
from .models import User




@csrf_exempt
def response(req):
	update = Update.de_json(json.loads(req.body.decode('utf-8')), bot)
	
	print(update)
	
	if update.effective_chat and update.effective_chat.type == Chat.PRIVATE:
		
		
		if update.callback_query:
			data = update.callback_query.data
			update.callback_query.answer()
			commands[data](update)
			
		else:
			if not update.effective_message.text in commands:
				update.effective_message.delete()
				return HttpResponse('')
			commands['/start'](update)	
	
			
	elif update.chat_member and update.chat_member.invite_link and not update.chat_member.invite_link.is_primary:

		
		invite_link = update.chat_member.invite_link.invite_link
		
		try:
			user = User.objects.get(id=update.effective_user.id)
			user.status = True
			
			if user.link == invite_link:
				#A user joining the group with his link is not counted
				user.save()
				return HttpResponse("")
				
			user.referral_link = invite_link
			user.save()
					
		except User.DoesNotExist:
			user = User.objects.create(id=update.effective_user.id, name = update.effective_user.name, referral_link = invite_link, status=True)
	
		
		try:
			referral = User.objects.get(link=invite_link)
			#update needed for overflow
			referral.referrees += 1
			referral.save()
				
			
			if referral.referrees==MAX_INVITE:
				text = f'{MAX_INVITE} persons have joined the group using your link.\nYou will be paid as soon as possible'
				bot.send_message(referral.id,text)
				bot.send_message(ADMIN_ID, f'{referral.name} has gotten {MAX_INVITE} referrals')
		except User.DoesNotExist:
				pass
				
				
	elif update.chat_member:
		
		if update.chat_member.invite_link:
			try:
				#Update the status of user
				user = User.objects.get(id=update.effective_user.id)
				user.status = True
				user.save()
			except User.DoesNotExist:
				pass
		
		result = extract_status_change(update.chat_member)
		
		if result:
			was_member, is_member = result
			if was_member and not is_member:
				#When a user leaves tue group
				try:
					#User is in registered
					user = User.objects.get(id=update.effective_user.id)
					referral_link = user.referral_link
				
					
					if user.link:
						#User has an invite link
						user.status = False
						user.referral_link = None
						user.save()
					else:
						#remove users without an invite link
						user.delete()
						
					
					##needs updating to check for overflow
					if referral_link:
						referral = User.objects.get(link=referral_link)
						referral.referrees -=1
						referral.save()
						
						
				except User.DoesNotExist:
					#user not in our database
					pass
			
        
	#print(update)
	return HttpResponse('')




def setWebHook(req):
	s = bot.set_webhook(f'{WEBHOOK_URL}bot/response/', allowed_updates=[Update.CHAT_MEMBER, Update.CALLBACK_QUERY, Update.MESSAGE], drop_pending_updates=True)
	if s:
		return redirect('admin:index')
	return HttpResponse('error')
	
def deleteWebHook(req):
	s = bot.delete_webhook()
	
	if s:
		return redirect('admin:index')
	return HttpResponse('error')
	
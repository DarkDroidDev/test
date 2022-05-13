from invite_bot.wsgi import bot
from invite_bot.config import GROUP_LINK, GROUP_ID
from .models import User
from .utils import translate

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.helpers import DEFAULT_20

keyboard = [
	[InlineKeyboardButton('Home  🏠', callback_data='/start'), InlineKeyboardButton('Detail  📈', callback_data='/detail')], 
	[InlineKeyboardButton('View Group  👥', url=GROUP_LINK)],
	[InlineKeyboardButton('About  💡', callback_data='/about')]
]

reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

		

def update_markup(update):
	lang = update.effective_user.language_code		
	txt = 'Home | Detail | View Group | About'
	data = translate(update, txt, 'keyboard')
	menus = data.split('\n\n')
	print(menus)
	texts = ['{}  🏠', '{}  📈', '{}  👥', '{} 💡']
	
	i = 0
	for r in keyboard:
		for btn in r:
			print(f'Index no: {i}')
			btn.text = texts[i].format(menus[i])
			i += 1
			
			
		
	
	


def start(update):
	
	lang = update.effective_user.language_code
	
	try:
		user = User.objects.get(id=update.effective_user.id)
		
		if not user.link:
			link = bot.create_chat_invite_link(GROUP_ID)
			user.link = link.invite_link
			user.save()
		
	except User.DoesNotExist:
		link = bot.create_chat_invite_link(GROUP_ID)
		
		user = User.objects.create(id=update.effective_user.id, link=link.invite_link, name=update.effective_user.name)
	
	
	text = translate(update,'Welcome to this test invite bot | Your invite link is: {} | Share your link and get rewarded when someone joins with your link', '/start').format(user.link)
	
	update_markup(update)
		
	if update.callback_query:
		query = update.callback_query
			
		query.edit_message_text(text=text, reply_markup = reply_markup)
		
	else:
		update.message.reply_text(text=text, reply_markup = reply_markup)
	
	
	
def detail(update):
	
	user = User.objects.get(pk=update.effective_user.id)
	text = translate(update,'{} person have joined the group using your link', '/detail').format(user.referrees)
	
	query = update.callback_query
	
	update_markup(update)
	
	query.edit_message_text(text=text, reply_markup = reply_markup)
	
	
	
def group(update):
	pass
	
	
def about(update):
	text = translate(update, 'This is an referral monitoring bot. It keeps record of people your refer to join the group. | The bot detects your language automatically. Change your telegram language and the bot will do the same!', '/about')
	
	query = update.callback_query
	
	
	update_markup(update)
	
	query.edit_message_text(text=text, reply_markup = reply_markup)
	
	
	

commands = {
	'/start': start,
	'/detail': detail,
	'/group': group,
	'/about': about
}
from telegram import ChatMember, ChatMemberUpdated
from urllib.parse import urlencode
import requests

from invite_bot.config import USE_TRANSLATOR_API, RAPID_API_KEY, RAPID_API_HOST
from .models import Translation

url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"


def extract_status_change(
    chat_member_update: ChatMemberUpdated,
):
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = (
        old_status
        in [
            ChatMember.MEMBER,
            ChatMember.CREATOR,
            ChatMember.ADMINISTRATOR,
        ]
        or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    )
    is_member = (
        new_status
        in [
            ChatMember.MEMBER,
            ChatMember.CREATOR,
            ChatMember.ADMINISTRATOR,
        ]
        or (new_status == ChatMember.RESTRICTED and new_is_member is True)
    )

    return was_member, is_member
    
    
 
    
def format_text(txt):
    return '\n\n'.join([x.strip() for x in txt.split('|')])   
    
def translate(update, txt, lookup):
    
    if update.effective_user.language_code=='en':
    	return format_text(txt)
    	
    	
    try:
    	translation = Translation.objects.get(lookup=lookup, lang=update.effective_user.language_code)
    	return format_text(translation.translated_text)
    	
    except Translation.DoesNotExist:
    	if not USE_GOOGLE_TRANSLATE:
    		return format_text(txt)
    
    	
    querystring = {"langpair":f"en|{update.effective_user.language_code}","q":txt,"mt":"1","onlyprivate":"0","de":"a@b.c"}
    
    headers = {
    "X-RapidAPI-Host": RAPID_API_HOST,
    "X-RapidAPI-Key": RAPID_API_KEY
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['responseData']['translatedText']
    
    translation = Translation.objects.create(lookup=lookup, lang=update.effective_user.language_code, translated_text=data)
    return format_text(data)
    
  
    
    
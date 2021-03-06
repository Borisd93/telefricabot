"""«Copyright 2021 Boris Daniel»
GPL v3 -> licence.txt"""
author='Boris Daniel Martinez Millán'
email='borisdanielmm@nauta.cu'
name='Reisub-Bot -> Friendicarg'

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,ReplyMarkup,Bot,user
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, CallbackContext
import api,crud,re,io,telegram
token="1531348810:AAG_ZWBHHPI4qxjeWvyWOwwy3xPXsN_2KJ0"

bot=Bot(token)
es={'pub':'Publicado con exito 😉',
'not_l_f':'Usted no esta logueado 😭',
'cha_l_f':'Su contraseña es incorrecta 😧',
'usa_l_f':'Usuario añadido 😎 ',
'usd_l_f':'Usuario eliminado 😭',
'usl_l_f':'Su usuario ya esta registrado 😎, para eliminarlo mande el comando /logout_f',
'usu_l_f':'El usuario o la contraseña esta mal,por favor enviame de nuevo el comando con el usuario y la contraseña',
'log_s_f':'usa esta sintaxis:\n/login_f Usuario contraseña',
'cls_l_f':'Tu publicación es muy pequeña o no tiene contenido'}
en={'pub':'Sucess!',
'not_l_f':'You not are logged in 😭',
'cha_l_f':'You password is incorrect 😧',
'usa_l_f':'User added 😎',
'usd_l_f':'User deleted 😭',
'usl_l_f':'Your user is registered 😎, for delete this please send me this comand /logout_f',
'usu_l_f':'The user or password is incorrect please send me again the comand with the user and password',
'welcome':'Hello and welcome to the Reisub Bot',
'thiss':'This bot contains some advancend functions of Reisub',
'suge':'This user: {} send a sugestion: {}',
'urown':'Please give me a link',
'urow1':'The link was created',
'log_s_f':'Use this sintax:\n/login_f user password',
'cls_l_f':'Your publication is clear or very short'}

def return_string(string,lang):
	if "es" in lang:
		return es[string]
	elif "en" in lang:
		return en[string]
	else:
		return es[string]

def log_friend(update: Update, context: CallbackContext) -> None:
	try:
		lan=io.open(update.effective_user.username,"r")
		lang=lan.read()
		lan.close()
	except:
		lang="es"
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	print(context.args)
	if len(context.args)<=1:
		update.message.reply_text(return_string('log_s_f',lang))
	else:
		try:
			friend=api.FriendApi("https://friendicarg.nsupdate.info/",context.args[0],context.args[1])
			crud.connect("friend_users.db")
			if len(crud.read("users","telegram",update.message.chat_id))==0:
				crud.create("users","'"+str(update.message.chat_id)+"','"+context.args[0]+"','"+context.args[1]+"'")
				update.message.reply_text(return_string('usa_l_f',lang))
			else:
				update.message.reply_text(return_string('usl_l_f',lang))
			crud.save();crud.close()
		except ValueError:
			update.message.reply_text(return_string('usu_l_f',lang))
	context.bot.delete_message(chat_id = update.message.chat_id, message_id = update.message.message_id)

def logout_friend(update: Update, context: CallbackContext) -> None:
	try:
		lan=io.open(update.effective_user.username,"r")
		lang=lan.read()
		lan.close()
	except:
		lang="es"
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	crud.connect("friend_users.db")
	if len(crud.read("users","telegram",update.message.chat_id))==1:
		crud.delete("users","telegram",str(update.message.chat_id))
		crud.save()
		crud.close()
		update.message.reply_text(return_string('usd_l_f',lang))
	else:
		update.message.reply_text(return_string('not_l_f',lang))
def publish(update: Update, context: CallbackContext) -> None:
	try:
		lan=io.open(update.effective_user.username,"r")
		lang=lan.read()
		lan.close()
	except:
		lang="es"
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	print(lang)
	crud.connect("friend_users.db")
	r=crud.read("users","telegram",update.message.chat_id)
	if len(r)==1:
		try:
			if '-' in str(update.message.chat_id):
				print('LOGGING DEBUG: RUNNING IN A GROUP, if this work please remove the line 93 of the code')
				friend=api.FriendApi("https://friendicarg.nsupdate.info/",r[0][1],r[0][2])
				contexto=update.message.text
				rex=re.findall("#!.*!#",contexto)
				if rex:
					rex=rex[0].replace("#!","").replace("!#","")
				else:
					rex=""
				a=re.findall('<.*>',contexto)
				if a:
					for i in a:
						contexto=contexto.replace(i,'[attachment type="link" url="'+i.replace("<","").replace(">","")+'"][/attachment]')
				del(a)
				a=re.findall('&.*&',contexto)
				if a:
					for i in a:
						contexto=contexto.replace(i,'[img='+i.replace("&","")+'][/img]')
				if "!horacu!" in contexto or "!horacu!" in rex:
					horacuvar=horacu()
					rex.replace("!horacu!",horacuvar)
					contexto.replace("!hora!",horavar).replace("!horacu!",horacuvar)
				if "!hora!" in contexto or "!hora!" in rex:
					horavar=time.strftime('%H:%M:%S')
					contexto.replace("!hora!",horavar).replace("!horacu!",horacuvar)
					rex.replace("!hora!",horavar)
				friend.share(rex,contexto.replace(rex,'').replace('/publish','')+"\n#telegram")
				update.message.reply_text(rex+'\n'+contexto.replace('/publish@reisub_bot','').replace('/publish ','').replace('#!'+rex+'!#',''))
				context.bot.delete_message(chat_id = update.message.chat_id, message_id = update.message.message_id)
			else:
				friend=api.FriendApi("https://friendicarg.nsupdate.info/",r[0][1],r[0][2])
				contexto=update.message.text
				rex=re.findall("#!.*!#",contexto)
				if rex:
					rex=rex[0].replace("#!","").replace("!#","")
				else:
					rex=""
				a=re.findall('<.*>',contexto)
				if a:
					for i in a:
						contexto=contexto.replace(i,'[attachment type="link" url="'+i.replace("<","").replace(">","")+'"][/attachment]')
					del(a)
				a=re.findall('&.*&',contexto)
				if a:
					for i in a:
						contexto=contexto.replace(i,'[img='+i.replace("&","")+'][/img]')
				if "!horacu!" in contexto or "!horacu!" in rex:
					horacuvar=horacu()
					rex.replace("!horacu!",horacuvar)
					contexto.replace("!hora!",horavar).replace("!horacu!",horacuvar)
				if "!hora!" in contexto or "!hora!" in rex:
					horavar=time.strftime('%H:%M:%S')
					contexto.replace("!hora!",horavar).replace("!horacu!",horacuvar)
					rex.replace("!hora!",horavar)
				friend.share(rex,(contexto.replace(rex,'').replace('/publish','')+"\n#telegram").replace('#!','').replace('!#',''))
				update.message.reply_text(return_string('pub',lang))
		except:
			update.message.reply_text(return_string('cha_l_f',lang))
	else:
		update.message.reply_text(return_string('not_l_f',lang))
def notifications(update:Update,context:CallbackContext):
	try:
		lan=io.open(update.effective_user.username,"r")
		lang=lan.read()
		lan.close()
	except:
		lang="es"
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	crud.connect("friend_users.db")
	r=crud.read("users","telegram",update.message.chat_id)
	if len(r)==1:
		friend=api.FriendApi("https://friendicarg.nsupdate.info/",r[0][1],r[0][2])
		update.message.reply_text(friend.notifications(5))
	else:
		update.message.reply_text(return_string('not_l_f',lang))

def get_5(update:Update,context:CallbackContext):
	try:
		lan=io.open(update.effective_user.username,"r")
		lang=lan.read()
		lan.close()
	except:
		lang="es"
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	crud.connect("friend_users.db")
	r=crud.read("users","telegram",update.message.chat_id)
	if len(r)==1:
		friend=api.FriendApi("https://friendicarg.nsupdate.info/",r[0][1],r[0][2])
		for i in range(0,4):
			update.message.reply_text(friend.network(5)[i].replace('><i class=icon-link icon-large><span class=sr-only',''))
	else:
		update.message.reply_text(return_string('not_l_f',lang))

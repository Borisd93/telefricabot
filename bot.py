"""«Copyright 2021 Boris Daniel»
GPL v3 -> licence.txt"""
author='Boris Daniel Martinez Millán'
email='borisdanielmm@nauta.cu'
name='Reisub-Bot'

try:
	from include import friendica_u,welcome,admin_id,token
except:
	raise ValueError('Hubo un error al importar el include.py')
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,ReplyMarkup,Bot,user
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, CallbackContext
#Importandk Friendica
from friendica_module import log_friend,logout_friend,publish,notifications
#Importando Uptime
from uptime_module import uptime
#Importando la base
import requests,io,random,re,api,crud,datetime,time,telegram
from os import remove
#Funcion base, no eliminar
def typing(chat):
	bot.send_chat_action(chat_id=chat, action=telegram.ChatAction.TYPING)

ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101'
ua += ' Firefox/60.0'
HEADERS = {'user-agent': ua}
help1=''
def log_function(dispatcher,name,function1):
	global help1
	dispatcher.add_handler(CommandHandler(name,function1)) 
	try:
		help1=help1+str('/'+name)+' -> '+function1.__doc__+'\n\n'
	except:
		help1=help1+str('/'+name)+' -> Not documented\n\n'

#Idioma español
es={'help':'''/start - Inicia el bot

/help - Muestra este menu
/short_url - Un acortador de URLs

/login_f - Logeate en tu cuenta de Friendicarg

/logout_f - Borra tu cuenta de la base de datos

/publish - Publica texto en tu cuenta de Friendica desde el cliente de Telegram''',
'pub':'Publicado con exito 😉',
'not_l_f':'Usted no esta logueado 😭',#
'cha_l_f':'Su contraseña es incorrecta 😧',#
'usa_l_f':'Usuario añadido 😎 ',#
'usd_l_f':'Usuario eliminado 😭',#
'usl_l_f':'Su usuario ya esta regtistrado 😎, para eliminarlo mande el comando /logout_f',#
'usu_l_f':'El usuario o la contraseña esta mal,por favor enviame de nuevo el comando con el usuario y la contraseña',#
'log_s_f':'usa esta sintaxis:\n/login_f Usuario contraseña',
'finish':'Exito'}


#Idioma ingles
en={'help':'''/start - Start the bot

/help - Show this menu

/short_url - A smaller url creator

/login_f - Login into your Friendicarg account

/logout_f - Delete your account from the database

/publish - Publish text into your Friendicarg account with telegram client''',
'pub':'Sucess!',
'not_l_f':'You not are logged in 😭',
'cha_l_f':'You password is incorrect 😧',
'usa_l_f':'User added 😎',
'usd_l_f':'User deleted 😭',
'usl_l_f':'Your user is registered 😎, for delete this please send me this comand /logout_f',
'usu_l_f':'The user or password is incorrect please send me again the comand with the user and password',
'log_s_f':'Use this sintax:\n/login_f user password',
'finish':'Sucess!'}

#Codigo base de todo abajo 
def return_string(string,lang):
	if "es" in lang:
		return es[string]
	elif "en" in lang:
		return en[string]
	else:
		return es[string]

def horacu():
	global x
	x = datetime.datetime.now()
	hora=int("%s" %x.hour)
	hora_aqui=22
	hora_s=hora+hora_aqui
	if hora_s>=25:
		hora_s=hora_s-24
	else:
		pass
	
	return str(hora_s)+":%s:%s" % (x.month, x.second)

try:
	crud.connect("friend_users.db")
	crud.runcode("""CREATE TABLE users(telegram INT,user STRING,password STRING)""")
	crud.save()
	crud.close() 
except:
	pass

bot=Bot(token)

def start(update:Update, context: CallbackContext) -> None:
	"""Inicia el Bot"""
	typing(update.message.chat_id)
	try:
		lan=io.open(update.effective_user.username,"r")
		lang=lan.read()
		lan.close()
	except:
		lang='es'
	try:
		update.message.reply_text(welcome[lang])
	except:
		update.message.reply_text(welcome['es'])

def sugerir(update:Update, context: CallbackContext) -> None:
	"""Sugiere que aladan algo o mejoren algo"""
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	try:
		lan=io.open(update.effective_user.username,"r")
		lang=io.read()
		lan.close()
	except:
		lang="es"
	bot.send_message(chat_id=admin_id,text="El personaje: @"+update.effective_user.username+" hizo una sugerencia: "+" ".join(context.args))
	update.reply_text(return_string('finish',))

def help(update:Update, context: CallbackContext) -> None:
	"""Devuelve esta ayuda"""
	update.message.reply_text(help1)


def set(update:Update, context: CallbackContext) -> None:
	if update.message.text.replace("/set ","").split(" ")[0]=="language":
		if "en" in update.message.text.replace("/set ","").split(" "):
			f=io.open(update.effective_user.username,"w")
			f.write("en")
			f.close()
			update.message.reply_text('Sucess')
		elif "es" in update.message.text.replace("/set ","").split(" "):
			f=io.open(update.effective_user.username,"w")
			f.write("es")
			f.close()
			update.message.reply_text('Exito')
		else:
			update.message.reply_text("You can help sending this comand /contribute\nPuedes contribuir mandando el comando /contribute")
if __name__=='__main__':
	updater=Updater(token=token)
	dispatcher=updater.dispatcher
	log_function(dispatcher,'start', start)
	log_function(dispatcher,'sugerencia', sugerir)
	log_function(dispatcher,'login_f', log_friend)
	log_function(dispatcher,'logout_f', logout_friend)
	log_function(dispatcher,'publish', publish)
	log_function(dispatcher,'help',help)
	log_function(dispatcher,'set',set)
	log_function(dispatcher,'notifications',notifications)
	log_function(dispatcher,'uptime',uptime)
	updater.start_polling()
	updater.idle()






import subprocess
from telegram import Update
from telegram.ext import Updater, CallbackContext

def uptime(update: Update,context: CallbackContext):
	"""Uptime es un modulo solo compatible con linux que permite ver el tiempo desde que se encendio la pc"""
	update.message.reply_text(subprocess.check_output('uptime',shell=True,universal_newlines=True))


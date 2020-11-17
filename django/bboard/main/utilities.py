from django.template.loader import render_to_string
from django.core.signing import Signer # Это для цифровой подписи
from bboard.settings import ALLOWED_HOSTS

from datetime import datetime
from os.path import splitext

signer = Signer()

def send_activation_notification(user): # Это для того чтобы отправлять только что зарегестрированому юзеру уведомление с потверждением аккаунта
	if ALLOWED_HOSTS:
		host = 'http://' + ALLOWED_HOSTS[0]
	else:
		host = 'http://localhost:8000'
	context = {'user':user, 'host':host, 'sign':signer.sign(user.username)} # Чтобы индефикатор был устойчив к подделке мы имя пользователя шифруем с помощью цифровой подписи
	subject = render_to_string('email/activation_letter_subject.txt', context) # Тема сообщения
	body_text = render_to_string('email/activation_letter_body.txt', context) # Тело сообщения 
	user.email_user(subject, body_text)

def get_timestamp_path(instance, filename): # Тк эта функция не относится не к редакторам не к контроллерами не к моделям ,мы просто запишем её сюда
	return f'{datetime.now().timestamp()}{splitext(filename)[1]}' # Эта функция будет генерировать названия для выгруженных файлов беря в рассчет текущее время и строку из названия файла

def send_new_comment_notification(comment): # Это функция которая отправляет уведомление пользователю о новых комментах
	if ALLOWED_HOSTS:
		host = 'http://' + ALLOWED_HOSTS[0]
	else:
		host = 'http://localhost:8000'
	author = comment.bb.author
	context = {'author':author, 'host':host, 'comment':comment}
	subject = render_to_string('email/new_comment_letter_subject.txt', context)
	body_text = render_to_string('email/new_comment_letter_body.txt', context)
	author.email_user(subject, body_text)
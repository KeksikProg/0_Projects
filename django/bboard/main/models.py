from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from django.db.models.signals import post_save

from .utilities import send_activation_notification
from .utilities import get_timestamp_path
from .utilities import send_new_comment_notification

class AdvUser(AbstractUser):
	is_activ = models.BooleanField(
		default = True, 
		db_index = True, 
		verbose_name = 'Прошёл активацию?')
	send_comment = models.BooleanField(
		default = True, 
		verbose_name = 'Слать оповещения о новых комментах?')

	def delete(self, *args, **kwargs): # Этот код для того чтобы если пользователь удалялся, то вместе с ним удалялись и объявления, которые он сделал
		for bb in self.bb_set.all():
			bb.delete()
		super().delete(*args, **kwargs)

	class Meta(AbstractUser.Meta):
		pass
#--------------------------------------------------------------------------------------------------------------------------
class Rubric(models.Model): # Это наша базовая модель от которой мы бдуем делать 2 прокси модели (надрубрики и подрубрики) (Прокси модель эта та в которой меняется только функциональность, а поля нет)
	name = models.CharField( # Название рубрики
		max_length = 20, 
		db_index = True, 
		unique = True, 
		verbose_name = 'Название')
	order = models.SmallIntegerField( # Порядок следования рубрики
		default = 0,
		db_index = True,
		verbose_name = 'Порядок')
	super_rubric = models.ForeignKey('SuperRubric', # И надрубрики (если это подрубрика)
		on_delete = models.PROTECT, # Защита от каскадного удаления
		null = True,
		blank = True,
		verbose_name = 'Надрубрика')
#--------------------------------------------------------------------------------------------------------------------------
class SuperRubricManager(models.Manager): # Это наш диспетчер записей для надрубрик (super_rubric)
	def get_queryset(self):
		return super().get_queryset().filter(super_rubric__isnull = True) # Будет возвращать только те записи где в поле super_rubric значение null (то есть надрубрики)

class SuperRubric(Rubric):
	objects = SuperRubricManager() # Тут мы объявляем менеджер записей

	def __str__(self):
		return self.name # Строковый вывод, который будет выводить в названии рубрики поле name 

	class Meta: 
		proxy = True # Значит что это прокси модель (в которой меняется только функциональность)
		ordering = ('order', 'name') # Поля по которым будет происходить поиск
		verbose_name = 'Надрубрика' # Название
		verbose_name_plural = 'Надрубрики' # Название в множественном числе
#--------------------------------------------------------------------------------------------------------------------------
class SubRibricManager(models.Manager): # Тут у нас менеждер записей ,который будет возвращать записи только где значение поля super_rubric не пустое (то есть есть надрубрика)
	def get_queryset(self):
		return super().get_queryset().filter(super_rubric__isnull = False) # По сути тут все тоже самое как и с надрубриками

class SubRubric(Rubric):
	objects = SubRibricManager()

	def __str__(self):
		return f'{self.super_rubric} - {self.name}'

	class Meta:
		proxy = True
		ordering = ('super_rubric__order', 'super_rubric__name', 'name', 'order') # Только тут стоит кое-что объяснить super_rubric__<поле> значит что поиск будет производится по полю(указанному после двойного подчеркивания) первичной модели
		verbose_name = 'Подрубрика'
		verbose_name_plural = 'Подрубрики'
#--------------------------------------------------------------------------------------------------------------------------
class Bb(models.Model):
	rubric = models.ForeignKey(
		SubRubric, 
		on_delete = models.PROTECT, # Чтобы вместе с удаление рубрики не удалилиьс объявления 
		verbose_name = 'Рубрика')
	title = models.CharField(
		max_length = 40, 
		verbose_name = 'Название товара')
	content = models.TextField(
		verbose_name = 'Описание')
	price = models.FloatField(
		default = 0, # Начальное значение 0
		verbose_name = 'Цена')
	contacts = models.TextField(
		verbose_name = 'Контакты')
	image = models.ImageField(
		blank = True, # Значит что поле может быть пустым
		upload_to = get_timestamp_path,
		verbose_name = 'Изображение')
	author = models.ForeignKey(AdvUser, 
		on_delete = models.CASCADE,
		verbose_name = 'Автор объявления')
	is_active = models.BooleanField(
		default = True,
		db_index = True,	
		verbose_name = 'Объявление активно?')
	created_at = models.DateTimeField(
		auto_now_add = True, # Активировать автоматическое заполнение
		db_index = True,
		verbose_name = 'Опубликовано')

	def delete(self, *args, **kwargs):
		for ai in self.additionalimage_set.all(): # Тут мы изменяем метод delete потому что перед удалением записи мы удаляем связанные с ней иллюстрации 
			ai.delete() # При данном методе возникает сигнал post_delete , который перехавтывает django_cleanup и удаляет иллюстрации 
		super().delete(*args, **kwargs)

	class Meta:
		verbose_name = 'Объявление'
		verbose_name_plural = 'Объявления'
		ordering = ['-created_at']

class AdditionalImage(models.Model):
	bb = models.ForeignKey(Bb,
		on_delete = models.CASCADE,
		verbose_name = 'Объявление')
	image = models.ImageField(
		upload_to = get_timestamp_path,
		verbose_name = 'Изображение')

	class Meta:
		verbose_name = 'Дополнительная иллюстрация'
		verbose_name_plural = 'Дополнительные иллюстрации'

class Comment(models.Model):
	bb = models.ForeignKey(
		Bb, 
		on_delete = models.CASCADE,
		verbose_name = 'Объявление')
	author = models.CharField(
		max_length = 30,
		verbose_name = 'Автор')
	content = models.TextField(
		verbose_name = 'Содержание')
	is_active = models.BooleanField(
		default = True,
		db_index = True,
		verbose_name = 'Выводить на экран?')
	created_at = models.DateTimeField(
		auto_now_add = True,
		db_index = True,
		verbose_name = 'Добавлено')

	class Meta:
		verbose_name_plural = 'Комментарии'
		verbose_name = 'Комментарий'
		ordering = ['created_at']

def post_save_dispatcher(sender, **kwargs):
	author = kwargs['instance'].bb.author
	if kwargs['created'] and author.send_comment:
		send_new_comment_notification(kwargs['instance'])
post_save.connect(post_save_dispatcher, sender = Comment)
#--------------------------------------------------------------------------------------------------------------------------
user_registrated = Signal(providing_args = ['instance']) # Тут мы из всех сигналов берем определенный по его ключу
def user_registrated_dispatcher(sender, **kwargs):
	send_activation_notification(kwargs['instance']) 
user_registrated.connect(user_registrated_dispatcher)
# Create your models here.

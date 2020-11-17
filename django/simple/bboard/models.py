from django.db import models
from django.contrib.auth.models import User
from django.core import validators

#----------------------------------------------------------------------------------------
class Bb(models.Model):
	title = models.CharField(max_length = 50, verbose_name = 'Название товара', validators = [validators.RegexValidator(regex = '')], error_messages = {'invalid':'Неправильное заполнение названия, уберите пожалуйста спец. символы'} ) # Текстовый тип данных, который говорит, что максимум 50 символов
	content = models.TextField(null = True, blank = True, verbose_name = 'Описание') # Тоже текстовый, но в этот раз неограничен по символам (необязателен к заполнению)
	price = models.FloatField(null = True, blank = True, verbose_name = 'Цена') # цифро-вещественный (необязателен)
	published = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = 'Дата публикации') # Дата и время (выставвляется само) db_index выставляет индексы в базе данных (понадобиться позже, когда будем соритровать по времени)
	rubric = models.ForeignKey('Rubric', null = True, on_delete = models.PROTECT, verbose_name = 'Рубрика') # Тут у нас связь один к многим (используется в выезжающем списке)
	
	def clean(self): # Данной функцией мы составляем валидацию модели (список ошибок)
		errors = {}
		if not self.content:
			errors['content'] = ValidationError('Укажите описание товара')

		if self.price and self.price < 0:
			errors['price'] = ValidationError('Укажите положительное число')

		if errors:
			raise ValidationError(errors)

		# Если мы хотим, чтобы сообщение относилось не какому-либо определенному полю, а ко всей модели, то мы делаем так
		# from django.core.exceptions import NON_FIELDS_ERROR
		# ... пишем, 
		# errors[NON_FIELDS_ERROR] = ValidationError('Ошибка в модели!')
	
	# verbose_name - Это, чтобы показывалось нормальное имя, а не, к примеру title

	class Meta:
		verbose_name_plural = 'Объявления' # Название модели в множественном числе
		verbose_name = 'Объявление' # Просто название модели
		ordering = ['-published'] # Соритровка полей по умолчанию
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
class Rubric(models.Model):
	name = models.CharField(max_length = 20, db_index = True, verbose_name = 'Название')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Рубрики'
		verbose_name = 'Рубрика'
		ordering = ['name']
#----------------------------------------------------------------------------------------
'''
class AdvUser(models.Model):
	is_activated = models.BooleanField(default = True)
	user = models.OneToOneField(User, on_delete = models.CASCADE) # Тут у нас свзять один к одному

class Spare(models.Model):
	name = models.CharField(max_length = 30)

class Machine (models.Model):
	name = models.CharField(max_length = 30)
	spares = models.ManyToManyField(Spare) # Тут у нас используется свзять многие к многим
'''
# Create your models here.

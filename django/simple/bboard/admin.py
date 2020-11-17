from django.contrib import admin
from django import forms
from django.db import models
from .models import Bb
from .models import Rubric
from django.urls import reverse

#@admin.register(Bb) Можно было сделать так, но уже сделано так что фиг с ним
class BbAdmin(admin.ModelAdmin):
	

	'''
	formfield_overrides = {
		models.ForeignKey : {'widget' : forms.widgets.Select(attrs = {'size' : 8})},
		}
	В общем, этот код делат так что элемент управления все полей с ForeignKey становится обычным списком м размером 8 ( у нас одно поле с ForeignKey и это rubric)
	'''
	'''
	def view_on_site(self, rec): # Данная функция делает так, чтобы рядом с формой объявления делает гиперссылку посмотреть на сайте
		return reverse ('bboard:detail', kwargs = {'pk': rec.pk})
		Но оно почему-то не работает так как надо
	'''
	fieldsets = ( # fieldsets - это атрибут который указывает в каком формате будут выводиться формы по созданию и правке на административном сайте
		(None, { # Название абзаца если None, то названия не будет
			'fields':(('title', 'rubric'), 'content'), # Кол-во полей, которые будут выводиться в форме title и rubric будут выводиться на одой строчке
			'classes': ('wide',), # Классы присваемые это набору полей
			}),
		('Дополнительные поля', { # Тут название уже есть 
				'fields': ('price',), # Поля которые будут вывсечиваться в данном наборе полей
				'classes':('collapse',), # Тут класс будет делать так что поля ,которые необязательные будут скрыты спойлером который можно раздвинуть
				'description': 'Поле необязательное для заполнения', # Дополнительная инфомация о том что поля необязательны для заполенния		
			})
					)

	#radio_fields = {'rubric':admin.VERTICAL} # Это элемент усправления, коорый делает выбор рубрики в виде выбора кружочка но я считаю, что он не удобный
	list_display = ('title', 'content','price','published', 'rubric') # list_display  атрибут который задает набор полей, которые будут выводится у данной модели на административном сайте
	list_display_links = ('content',) # из названия и описания делает гиперссылку, перейду по которой можно будет изменить данные 
	list_editable = ('title', 'price') # Дает возможность изменять данные этих полей не переходя на страницу правки 
	search_fields = ('title', 'content') # Добавляет на админ. сайт поиск по даные полям 

admin.site.register(Rubric)
admin.site.register(Bb, BbAdmin) # Регистрирует модель и редактор которым она будет регулироваться в данном случае модель Bb будет регулироваться редактором BbAdmin
# Register your models here.

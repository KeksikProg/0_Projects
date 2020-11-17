'''
В данном файле по негласному соглашению среди рпограммистов содержатся сериализаторы (смотреть параметры для полей в моделях)
'''
from rest_framework import serializers
from .models import Rubric

class RubricSerializer(serializers.ModelSerializer): # Создаем серилизатор для рубрик 
	class Meta: # Уже знакомый нам класс Meta
		model = Rubric # Связываем серилизатор с моделью 
		fields = ('id','name') # и указываем какие поля будут создаваться 
		# Далее мы перемещаемся в views и на основе этого сериализатора создаем функцию api_rubric
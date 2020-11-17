'''
Сериализатор - это штука которая позволяет превратить какую либо структуру
в поток битов в формате JSON чаще всего и потом просто получить ту же самую структуру на выходе
'''
from rest_framework import serializers

from main.models import Bb
from main.models import Comment


class BbSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bb
		fields = (
			'id', 
			'title', 
			'content', 
			'price', 
			'created_at')


class BbDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bb
		fields = (
			'id', 
			'title', 
			'content', 
			'price', 
			'created_at', 
			'contacts', 
			'image')


class CommentSerializer(serializers.ModelSerializer):
	class Meta:	
		model = Comment
		fields = (
			'bb', 
			'author', 
			'content', 
			'created_at')

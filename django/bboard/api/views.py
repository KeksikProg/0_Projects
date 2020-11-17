from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from main.models import Bb
from main.models import Comment
from .serializers import BbSerializer
from .serializers import BbDetailSerializer
from .serializers import CommentSerializer

@api_view(['GET']) # Это значит что это функция будет воспринимать только запросы GET
def bbs(request):
	if request.method == 'GET':
		bbs = Bb.objects.filter(is_active = True)[:10] # Тут мы просто передаем первые 10 объявлений
		serializer = BbSerializer(bbs, many = True) # Тут у нас наш сериализатор вместе с переменной в которой будут наши 10 объявлений
		return Response(serializer.data) # Просто возвращаем результат сериализатора

class BbDetailView(RetrieveAPIView): # Тут у нас контроллер который будет выводить детальные сведения о объявлении
	queryset = Bb.objects.filter(is_active = True) # Отбираем объявления которые нам нужны (только те что активные это понятно)
	serializer_class = BbDetailSerializer # А тут сериализатор которым мы будем передавать наши данные 

@api_view(['GET', 'POST']) # Функция будет воспринимать только запросы POST, GET
@permission_classes((IsAuthenticatedOrReadOnly,)) # К запросу POST мы допустим только зарегестрированных польхователей, а к запросу GET может получить любой желающий
def comments(request, pk):
	if request.method == 'POST': # Если запрос POST (Человек хочет оставить комментарий)
		serializer = CommentSerializer(data = request.data) #Значит оформляем сериализатор 
		if serializer.is_valid():# И если он правильно заполнен
			serializer.save() # То сохраняем его
			return Response(serializer.data, status = HTTP_201_CREATED) 
		else: # Иначе выдаем ошибку 
			return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)
	else: # Если же человек хочет просто посмотреть комментарии, то не отказываем ему и просто даем
		comments = Comment.objects.filter(is_active = True, bb = pk)
		serializer = CommentSerializer(comments, many = True)
		return Response(serializer.data)






# Create your views here.

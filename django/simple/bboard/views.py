from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.dates import ArchiveIndexView
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import success

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Bb, Rubric
from .forms import BbForm
from .serializers import RubricSerializer


#----------------------------------------------------------------------------------------
def bb_lmf(request, pk): #Эта функция для кэша класса снизу (СМОТРЕТЬ URLS ПРИЛОЖЕНИЯ)
	return Bb.objects.get(pk = pk).published #Если дата публикации не изменилась, значит берет из кэша страницу

class BbDetailView(DetailView): # Для того чтобы увидеть детали объявления 
	model = Bb

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def index(request): # Начальная страница сайта (полная доска объявлений)
	bbs = Bb.objects.all()
	rubrics = Rubric.objects.all()
	paginator = Paginator(bbs, 3) # Пагинатор (2 объявления на странице максимум)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {'bbs':page.object_list, 'rubrics':rubrics, 'page':page}
	return render (request, 'bboard/index.html', context)
#----------------------------------------------------------------------------------------
	#Это мертвый код, он пока не нужен
#----------------------------------------------------------------------------------------
'''
class BbCreateView(SuccessMessageMixin, CreateView):
	template_name = 'bboard/create.html' # Путь к файлу шаблона, где находится форма
	form_class = BbForm # Сама форма
	success_url = reverse_lazy('index') # Сайт на который будет переправлять после успешного заполнения формы
	success_message = 'Объявление "%(title)s" успешно создано' #Всплывающее сообщение о том что объявление было создано

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['rubric'] = Rubric.objects.all()
		return context
'''
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def by_rubric(request, rubric_id):
	bbs = Bb.objects.filter(rubric = rubric_id)
	rubrics = Rubric.objects.all()
	current_rubric = Rubric.objects.get(pk = rubric_id)
	context = {'bbs':bbs, 'rubrics':rubrics, 'current_rubric':current_rubric}
	return render(request, 'bboard/by_rubric.html', context)
#----------------------------------------------------------------------------------------
	#Код выше и код ниже связаны между собой 
#----------------------------------------------------------------------------------------
def add_and_save (request): # выводит форму ,и сохраняет в базу данные веденные пользователем
	if request.method == 'POST': # Проверяет, чтобы метод был пост, тк пост это принятие данных от пользователя
		bbf = BbForm(request.POST) # создаем форму 
		if bbf.is_valid(): # если форма правильно заполнена то 
			bbf.save() # сохраняем её
			success(request, 'Объявление {} в рубрике {} было успешно создано'.format(bbf.cleaned_data['title'], bbf.cleaned_data['rubric']))
			return by_rubric(request, bbf.cleaned_data['rubric'].pk)
			#return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs = {'rubric_id' : bbf.cleaned_data['rubric'].pk})) # а пользователя отправляем на страницу рубрики ,которую он заполнял

		else:
			context = {'form':bbf} # если в заполнении таблицы были проблемы, то
			return render(request, 'bboard/create.html', context) # пользователя отправит заного заполнять страницу
	else:
		bbf = BbForm() # если метод не пост, то
		context = {'form':bbf} 
		return render(request, 'bboard/create.html', context) # отправляем пользователя на заполнение страницы
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
class BbEditView(SuccessMessageMixin, UpdateView): # Для изменения объявления 
	model = Bb # Модель в которой будут происходит изменения
	form_class = BbForm # Форма в которую первоначальо занасились данные 
	success_url = '/bboard' # Адрес куда будет перенапрвлен пользователь после смены данных
	success_message = 'Обявление "%(title)s" успешно изменено' # Тут нельзя почему-то использовать format

	def get_context_data (self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
class BbDeleteView(SuccessMessageMixin, DeleteView): # Для удаления объявления 
	model = Bb # Модель в которой будут удалятся данные
	success_url = '/bboard' # Адрес куда будет перенапрвлен пользователь после удаления данных
	success_message = 'Объявление "%(title)s" успешно удалено' # Тут нельзя почему-то использовать format

	def get_context_url(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context
#----------------------------------------------------------------------------------------
@api_view(['GET']) # Специльный декратор, который позволяет выводить данные в удобном и читаемом виде
def api_rubrics(request): # Это для того чтобы если какое-либо прилоежние запросил рубрики, то он получил их в формате Json
	if request.method == 'GET': # Если метод гет значит пользователь хочет прочитать
		rubrics = Rubric.objects.all() # Заносим в переменную все рубрики
		serializer = RubricSerializer(rubrics, many = True) #Создаем сериализатор 
		return Response(serializer.data) # И просто отправляем клиенту в формате Json

@api_view(['GET'])
def api_rubric_detail(request, pk): # Это для того чтобы получать детальные сведения о какой-лбио рубрике при её запросе каким-либо приложением
	if request.method == 'GET':
		rubric = Rubric.objects.get(pk = pk)
		serializer = RubricSerializer(rubric)
		return Response(serializer.data)

# Create your views here.

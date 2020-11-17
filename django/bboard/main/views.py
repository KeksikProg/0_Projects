from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect

from .utilities import signer
from .forms import RegisterUserForm
from .models import AdvUser
from .forms import ChangeUserInfoForm
from .models import SubRubric, Bb
from .forms import SearchForm
from .forms import BbForm, AIFormSet
from .models import Comment
from .forms import UserCommentForm, GuestCommentForm


def index(request): # Это наша начальная страница 
	bbs = Bb.objects.filter(is_active = True)[:10]
	context = {'bbs':bbs}
	return render (request, 'main/index.html', context)


def other_page(request, page): # Это будет наша страница со скучными бумагами
	try:
		template = get_template('main/' + page + '.html') # Пытаемся получить шаблон
	except TemplateDoesNotExist: # Если не находит такуб страницу
		raise Http404 # То ошибка 404 (страница не найдена)
	return HttpResponse(template.render(request = request)) # Иначе вернуть ответ клиенту


class BBLoginView(LoginView): # Это будет просто страница авторизации на сайте
	template_name = 'main/login.html'  # шаблон который будет браться для авторизации


@login_required # Делает страницу доступной только зарегестрированным пользователям
def profile(request):
	bbs = Bb.objects.filter(author=request.user.pk)
	context = {'bbs' : bbs}
	return render (request, 'main/profile.html', context)


class BBLogoutView(LogoutView, LoginRequiredMixin): #Здесь класс LRM для того чтобы страница выода была доступна только авторизованым пользователям
	template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):

	model = AdvUser  # Модель из которой будет извлекаться запись
	template_name = 'main/change_user_info.html' # шаблон который будет 
	form_class = ChangeUserInfoForm # Форма 
	success_url = reverse_lazy('main:profile') # Куда будет перенаправлен человек после смены данных
	success_messsage = 'Личные данные пользователя были успешно изменены!' # Всплывающее сообщение которое получит человек после смены своих данных

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk # Чтобы получить данные пользователя из модели нам нужно знать данные какого именно пользователя мы хотим получить и для этого извлекаем его user_id
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None): # Проверяем была ли передана модель самим юзером и если нет то сами её берем
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView): # 1 класс это всплывающее сообщение 2 класс чтобы контроллер был доступен только зареганым и 3 класс для смены пароля
	template_name = 'main/password_change.html' #Шаблон
	success_url = reverse_lazy('main:profile') #Перенаправление
	success_messsage = 'Пароль пользователя изменен!' #Сообщение


class RegisterUserView(CreateView): # класс в суперклассах для создания новых объектов и рендера шаблонов
	model = AdvUser
	template_name = 'main/register_user.html'
	form_class = RegisterUserForm
	success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView): # Это класс для вывода страницы о том что пользователь успешно создан и его нужно потвердить, а суперкласс чисто для вывода шаблона отрендеренного
	template_name = 'main/register_done.html'


def user_activate(request, sign): # Это контроллер для потверждения пользователем 
	try:
		username = signer.unsign(sign) # Пытаемся раcшифровать
	except BadSignature: # Если не получается
		return render (request, 'main/bad_signature.html') # Говорим что плохая сигнатура
	user = get_object_or_404(AdvUser, username = username) # если все получается, то берем из модели username или если такого нет то ошибка 404
	if user.is_active: # В случае если юзер уже активирован шлем сообщение что он уже прошёл активацию
		template = 'main/user_is_activated.html'
	else:
		template = 'main/activation_done.html'
		user.is_active = True
		user.save()
	return render (request, template)

class DeleteUserView(LoginRequiredMixin, DeleteView): # Это класс для удаления пользователя (потому что если можно создать, значит должно быть можно и удалить)
	model = AdvUser
	template_name = 'main/delete_user.html'
	success_url = reverse_lazy('main:index')

	def dispatch (self, request, *args, **kwargs):
		self.user_id = request.user.pk # Тут мы просто получаем id пользователя 
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logout(request) # Осуществляем выход (потому что пока в аккаунте кто-то есть его нельзя удалить)
		messages.add_message(request, messages.SUCCESS, 'Пользователь успешно удален!') # Добавляем сообщение о том что пользователь успешно удален
		return super().post(request, *args, **kwargs)

	def get_object(self, queryset = None): # Тут как и раньше мы просто в моделях находим пользователя по user_id, которого нужно удалить
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)

def by_rubric(request, pk): # Это функция для просмотров объявлений определенной рубрики а не всех
	rubric = get_object_or_404(SubRubric, pk = pk) # Пытаемся получить рубрику по pk если не получается то просто выводит ошибку 404
	bbs = Bb.objects.filter(rubric = rubric, is_active = True) # Выбрать только те объявления, которые активные 
	if 'keyword' in request.GET: # Если в гет запросе пользователя есть keyword , то есть искомое слово
		keyword = request.GET['keyword'] # То мы берем это слово
		q = Q(title__icontains = keyword) | Q(content__icontains = keyword) # Если слово попадается либо в названии либо в описании
		bbs = bbs.filter(q) # И фильтруем все объявления на это слово
	else:
		keyword = '' # Иначе если куйворда нет, то 
	form = SearchForm(initial = {'keyword':keyword}) # Мы просто показываем все объявления
	paginator = Paginator(bbs, 2) # Наш пагинатор, который будет выводить только по 2 объявления
	if 'page' in request.GET: # Если в гет запросе есть страница
		page_num = request.GET['page'] # То мы её извлекаем
	else: #если нет, то просто
		page_num = 1 # будет страница 1
	page = paginator.get_page(page_num) # 'Говорим' пагинатору какая страница
	context = { # А тут контекст
		'rubric' : rubric, 
		'page' : page, 
		'bbs' : page.object_list, # Все объявления
		'form' : form}
	return render (request, 'main/by_rubric.html', context)

def detail(request, rubric_pk, pk):
	bb = Bb.objects.get(pk = pk)
	ais = bb.additionalimage_set.all() # Тут мы вместе с объявлением подготваливаем список дополнительных иллюстраций
	comments = Comment.objects.filter(bb = pk, is_active = True)
	initial = {'bb' : bb.pk}
	if request.user.is_authenticated:
		initial['author'] = request.user.username
		form_class = UserCommentForm
	else:
		form_class = GuestCommentForm
	form = form_class(initial = initial)
	if request.method == 'POST':
		c_form = form_class(request.POST)
		if c_form.is_valid():
			c_form.save()
			messages.add_message(request, messages.SUCCESS, 'Комментарий успешно добавлен')
		else:
			form = c_form
			messages.add_message(request, messages.WARNING, 'Комментарий не был добавлен')
	context = {'bb':bb, 'ais':ais, 'comments':comments, 'form':form}
	return render (request, 'main/detail.html', context)

@login_required
def profile_bb_add(request): # Для создания объявлений обычными юзерами
	if request.method == 'POST': # Метод должен быть пост потому что мы заносим данные в модель
		form = BbForm(request.POST, request.FILES) # request.files мы передаем потому что если так не сделать, то дополнительные иллюстрации потеряются
		if form.is_valid(): # Проверяем верно ли была заполнена форма
			bb = form.save() # И если да, то сохраняем её
			formset = AIFormSet(request.POST, request.FILES, instance = bb) # Тут мы передаем объявление третим аргументом чтобы дополнительные иллюстрации были связаны с объявлением
			if formset.is_valid(): # Опять проверяем
				formset.save() # И уже окончательно сохраняем
				messages.add_message(request, messages.SUCCESS, message = 'Объявление успешно добавлено!') # Пользователю высвечивается сообщение о том что все успешно сохранено
				return redirect('main:profile') # И его перенаправляет на свой профиль
	else:
		form = BbForm(initial = {'author':request.user.pk})
		formset = AIFormSet()
	context = {'form' : form, 'formset' : formset}
	return render(request, 'main/profile_bb_add.html', context)

@login_required
def profile_bb_change(request, pk):
	bb = get_object_or_404(Bb, pk = pk)
	if request.method == 'POST':
		form = BbForm(request.POST, request.FILES, instance = bb)
		if form.is_valid():
			bb = form.save()
			formset = AIFormSet(request.POST, request.FILES, instance = bb)
			if formset.is_valid():
				formset.save()
				messages.add_message(request, messages.SUCCESS, message = 'Объявление успешно изменено!')
				return redirect ('main:profile')
	else:
		form = BbForm(instance = bb)
		formset = AIFormSet(instance = bb)
	context = {'form' : form, 'formset' : formset}
	return render (request, 'main/profile_bb_change.html', context)

@login_required
def profile_bb_delete(request, pk):
	bb = get_object_or_404(Bb, pk = pk)
	if request.method == 'POST':
		bb.delete()
		messages.add_message(request, messages.SUCCESS, message = 'Объявление успешно удалено!')
		return redirect('main:profile')
	else:
		context = {'bb' : bb}
		return render (request, 'main/profile_bb_delete.html', context)



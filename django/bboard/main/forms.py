from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import Bb, AdditionalImage
from captcha.fields import CaptchaField

from .models import Comment
from .models import AdvUser
from .models import user_registrated
from .models import SuperRubric, SubRubric

class ChangeUserInfoForm(forms.ModelForm):
	email = forms.EmailField(required = True, label = 'Адрес электронной почты')

	class Meta:
		model = AdvUser
		fields = ('username', 'email', 'first_name', 'last_name', 'send_comment')

class RegisterUserForm(forms.ModelForm): # Тут у нас форма, которая будет использоваться при регистрации пользователя
	# Тут с помощью метода полного объявления объявляем поля почты и паролей (полное объявление мы делаем потому что хотим, чтобы эти поля были обязательными для заполения)
	email = forms.EmailField(
		required = True, # Значит что поле обязательно для заполнения 
		label = 'Адрес электроной почты') # Название поля в форме
	password1 = forms.CharField(
		label = 'Пароль', 
		widget = forms.PasswordInput, # Меню управления данным полем
		help_text = password_validation.password_validators_help_text_html(),) # Выводит дополнительную информацию какие символы могут быть в пароле а какие нет
	password2 = forms.CharField(
		label = 'Пароль (повторно)',
		widget = forms.PasswordInput,
		help_text = 'Введите тот же самый пароль ещё раз')

	def clean(self): # Тут мы проверяем чтобы пароли из двух полей были одинаковыми 
		password1 = self.cleaned_data['password1']
		if password1:
			password_validation.validate_password(password1)
		super().clean()
		password2 = self.cleaned_data['password2']
		if password1 and password2 and password1 != password2: # Честно я не знаю зачем делать такой if
			errors = {'password2':ValidationError(
				'Введенные пароли не совпадают', 
				code = 'password_mismatch')}
			raise ValidationError(errors)

	def save(self, commit = True): # Тут мы уже оформляем сохранение пользователя
		user = super().save(commit = False) # Метод save уже как бы есть так что мы его переопределяем
		user.set_password(self.cleaned_data['password1'])
		user.is_active = False # Значит что пользователь не активный
		user.is_activated = False # Пользователь не прошёл проверку на активность 
		if commit:
			user.save()
		user_registrated.send(RegisterUserForm, instance = user) # И тут мы тправляем сигнал, чтобы пользователю отправилось сообщение на электронную почту для потверждения
		return user

	class Meta:
		model = AdvUser
		fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_comment') # Тут мы просто объявляем поля которые должны быть в форме

class SubRubricForm(forms.ModelForm): # Это форма для создания подрубрик
	super_rubric = forms.ModelChoiceField(
		queryset = SuperRubric.objects.all(), # Тут мы делаем полное объявление чтобы сказать, что поле надрубрика для подрубрики должно быть обязательно заполнено
		empty_label = None, # Этим параметром мы у раскрывающегося списка убрали пункт ----, сказав что надрубрика должна быть
		label = 'Надрубрика',
		required = True,)

	class Meta:
		model = SubRubric
		fields = '__all__'

class SearchForm(forms.Form): # Эта форма не привязанна к никакой модели, мы её будем использовать для поиска на сайте
	keyword = forms.CharField( 
		required = False,
		max_length = 20,
		label = '')

class BbForm(forms.ModelForm):
	class Meta:
		model = Bb
		fields = '__all__'
		widgets = {'author' : forms.HiddenInput}

AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields = '__all__')

class UserCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ('is_active',)
		widgets = {'bb':forms.HiddenInput}

class GuestCommentForm(forms.ModelForm):
	captcha = CaptchaField(
		label = 'Введите слово с картинки',
		error_messages = {'invalid':'Введенное слово неверно, попробуйте снова'})

	class Meta:
		model = Comment
		exclude = ('is_active',)
		widgets = {'bb':forms.HiddenInput}
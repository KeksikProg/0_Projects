from django.urls import path

from .views import index, other_page
from .views import BBLoginView
from .views import profile
from .views import BBLogoutView
from .views import ChangeUserInfoView
from .views import BBPasswordChangeView
from .views import RegisterUserView, RegisterDoneView
from .views import user_activate
from .views import DeleteUserView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from .views import by_rubric
from .views import detail
from .views import profile_bb_add
from .views import profile_bb_delete, profile_bb_change

app_name = 'main'
urlpatterns = [
	path('accounts/profile/change/<int:pk>', profile_bb_change,
		name = 'profile_bb_change'),
	path('accounts/profile/delete/<int:pk>', profile_bb_delete,
		name = 'profile_bb_delete'),
	path('accounts/profile/add/', profile_bb_add, # Это для создания объявлений обычными юзерами
		name = 'profile_bb_add'),
	path('<int:rubric_pk>/<int:pk>/', detail, 
		name = 'detail'),
	path('<int:pk>/', by_rubric, # Важно поместить данный код перед other_page, потому что если этого не сделать будут конфликты
		name = 'by_rubric'),
	path('<str:page>/', other_page, 
		name = 'other'),
	path('', index, # Тут у нас функция 
		name = 'index'),
	path('accounts/login/', BBLoginView.as_view(), 
		name = 'login'),
	path('accounts/profile/', profile, 
		name = 'profile'),
	path('accounts/logout/', BBLogoutView.as_view(), 
		name = 'logout'),
	path('accounts/profile/change/', ChangeUserInfoView.as_view(), 
		name = 'profile_change'),
	path('accounts/password/change/', BBPasswordChangeView.as_view(), 
		name = 'password_change'),
	path('accounts/register/done/', RegisterDoneView.as_view(),
		name = 'register_done'),
	path('accounts/register/', RegisterUserView.as_view(),
		name = 'register'),
	path('accounts/register/activate/<str:sign>/', user_activate,
		name = 'register_activate'),
	path('accounts/profile/delete', DeleteUserView.as_view(),
		name = 'profile_delete'),
	path('accounts/profile/reset/email_reset', PasswordResetView.as_view( # Для отправки писем о смене пароля
		template_name = 'main/email_reset_password.html',
		subject_template_name = 'email/reset_password_subject.txt',
		email_template_name = 'email/reset_password_body.html',
		success_url = 'email_done'),
		name = 'email_reset'),
	path('accounts/profile/reset/email_done', PasswordResetDoneView.as_view( # Для оповещение что письмо успешно отпрвлено
		template_name = 'main/email_done.html',),
		name = 'password_reset_done'),
	path('accounts/profile/reset/reset_password/<uidb64>/<token>', PasswordResetConfirmView.as_view( # Сама смена пароля
		template_name = 'main/reset_password.html',
		success_url = reverse_lazy('main:index')), 
		name = 'reset_password'),
]
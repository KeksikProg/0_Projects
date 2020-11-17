"""simple URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, LogoutView
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('admin/', admin.site.urls), # Админский сайт
    path('bboard/', include('bboard.urls')), # главная страница, то есть доска объявлений
    path('accounts/login/', LoginView.as_view(), name = 'login'), #для входа на профиль 
    path('accounts/login/', LogoutView.as_view(next_page = 'bboard:index'), name = 'logout'), # для выхода с профиля 
    path('accounts/password_reset/', PasswordResetView.as_view( # на страницу с формой в которую элетронную почту
    	template_name = 'registration/reset_password.html',
    	subject_template_name = 'registration/reset_subject.txt',
    	email_template_name = 'registration/reset_email.html',), name = 'password_reset'),
    path('accounts/reset/<uid64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'registration/confirm_password.html'), name = 'password_reset_confirm'), # ссылка для сброса пароля 
    path('captcha/', include('captcha.urls')), # для капчи
    #path('social/', include('social_django.urls', namespace = 'social')), # для входа с помощью социальных сетей
]

#if settings.DEBUG:
    #urlpatterns.append(path('static/<path:path>', never_cache(serve)))

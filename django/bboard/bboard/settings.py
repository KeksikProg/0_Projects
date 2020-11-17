"""
Django settings for bboard project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

AUTH_USER_MODEL = 'main.AdvUser'

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Папка куда будут складироваться медиа файлы 
MEDIA_URL = '/media/' # Префикс по которому джанго будет понимать, что дальше идет медиа файл


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q63gzjh^l#(i#6f($mxmy1$_-=l_0pp5-8+k_p1zlwsxj-=u=g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SOCIAL_AUTH__OAUTH2_WHITELISTED_DOMAINS = []


CORS_ORIGIN_ALLOW_ALL = True # Дает доступ с любого домена
CORS_URLS_REGEX = r'^/api/.*$' # Но только к тому что идет после url api
# Application definition
#Все что ниже это для отправки писем 
EMAIL_PORT = 465 # Порт через который будут отправляется письма
EMAIL_USE_SSL = True # Использовать ли протокол шифрования SSL
EMAIL_HOST = 'smtp.gmail.com' # Какой протокол SMTP использовать
EMAIL_HOST_USER = 'bbboarddd@gmail.com' # Почта с которой будут отправлятся все письма
EMAIL_HOST_PASSWORD = '1234567812345678' # Пароль от это почты


SOCIAL_AUTH_VK_OAUTH2_KEY = '7476993' # Секретный ключ который берется из приложения вконтакте
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'rHAOQYOdYQfsXCQUjqPC'# тоже ключ и тоже берется из приложения 

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email'] # Чтобы дополнительно запросить у пользователя почту 

AUTHENTICATION_BACKENDS = ( # Список классов реализующий аутентефикацию и авторизацию
    'social_core.backends.vk.VKOAuth2', # Это и ниже для авторизации с помощью вк
    'django.contrib.auth.backends.ModelBackend',

)

THUMBNAIL_ALIASES = {
	'' : {
		'default' : {
			'size' : (96, 96), # Размер миниатюр 
			'crop' : 'scale',
		}
	}
}
THUMBNAIL_BASEDIR = 'thumbnails' # Место где будут храниться только миниатюры

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig', #Наше приложение
    'bootstrap4', # Это CCS фреймворк для быстрого создания страниц
    'social_django', #Это для авторизации через соц сети
    'django_cleanup', # Это для того, чтобы файлы которые привязаны к записи в модели удалялись вместе с записью
    'easy_thumbnails', # Это для того чтобы у объявлений были миниатюры (маленькие изображения)
    'captcha', # Для того чтобы было можно использовать капчу
    'rest_framework', # Для того чтобы использовать структуру REST
    'corsheaders', # Для того чтобы проект мог давать доступ к api другим доменам
    'api.apps.ApiConfig' # Наше новое приложение api
]

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware', # Для библиотеки corsheaders
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', # это и одно ниже для регистрации через соц сети
                'social_django.context_processors.login_redirect',
                'main.middlewares.bboard_context_processor', # Наш свобственный посредник
            ],
        },
    },
]

WSGI_APPLICATION = 'bboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'bboard.data'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

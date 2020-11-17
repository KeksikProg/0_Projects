"""
Джанго настройки для проекта <simple>.

Сгенерирован с помощью 'django-admin startproject' использует джанго 3.0.5.

Чтобы получить больше информации о проекте смотреть:
https://docs.djangoproject.com/en/3.0/topics/settings/

Для просмтора полного списка настроек и значений смотерть:
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Строит путь к папке проекта (делает это автоматически)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g5z3wxe3bu31-j-2@($62m9=!st4qg8@s&*q1%l*-4@4ukeu-a'
#(КАРАМБА АЛЯРМ)Секретный ключ, который используется в шифровании джанго (не сообщать никому)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#(КАРАМБА АЛЯРМ) запускает режим откладки сайта (аккуратно, не включать в готовый проект)
# В этом режиме при какой либо ошибке сайт показывает проблему детально (если режим выключен, то просто показывает код ошибки)

ALLOWED_HOSTS = [] # Список хостов с которы джанго будет принимать сообщения

'''
Тут будут настройки, которые можно добавить дополнительно
STATIC_ROOT - Можно изменить путь к статическим файлам сайтам os.path.join(BASE_DIR, 'static')
MEDIA_ROOT - Можно изменить папку выгрузки файлов клиента
CACHES - Следует указать параметр кэширование сервера
LOGGING - Указать окончательные средства диагностики
ADMINS - Электронные почты админов
MANAGERS - Электронные почты менеждеров
'''
# Application definition

INSTALLED_APPS = [ # Все приложения, которые используются на сайте
    'bboard.apps.BboardConfig', # Наше приложение доска
    'django.contrib.admin', # Реализует администарцию на сайте
    'django.contrib.auth', # Разграничивает доступ по сайту (используется приложением выше)
    'django.contrib.contenttypes', # Хранит список всех моделей (баз данных)
    'django.contrib.sessions', # обеспечивает хранение данных клиента на стороне сервера
    'django.contrib.messages', # Используется для обработки всплывающих сообщений
    'django.contrib.staticfiles', # Реализует обработку статических файлов (те файлы, которые отправляются клиенту без обработки (фотки, css, и тп))
    'captcha', # Это, чтобы использовать капчу
    'precise_bbcode', # Это, чтобы использовать BBCode
    'social_django', #Чтобы использовать авторизацию через вконтакте
    'rest_framework', # Для того чтобы использовать Django REST Framework
    'corsheaders', # Для того чтобы джанго смог обрабатывать запросы пришедшие с разных доменов а не только с нашего

]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

SOCIAL_AUTH_VK_OAUTH2_KEY = '7476993' # id для приложения в вконтакте
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'YZM8Z8iEpAGxeL7PHxMV' # защищенный ключ для приложения в вконтакте
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email'] # Чтоыб помимо других данных получать от пользователя его адрес электроной почты

CORS_ORIGIN_ALLOW_ALL = True # Джанго будет обрабатывать запросы, которые приходят с любого домена
CORS_URLS_REXEG = r'^/api/.*$' # Показывает то что запросы приходящие с доменов могут получить доступ только к API и далее

MIDDLEWARE = [ # тут содержатся посредники, они выполняют предварительную обработку запроса прежде чем передвавть её контроллеру
    'django.middleware.security.SecurityMiddleware', # Реализует дополнительную защиту сайта от сетевых атак
    'django.contrib.sessions.middleware.SessionMiddleware', # обеспечивает работу сессий на низком уровне (используется администратором, всплывающими сообщениями)
    'corsheaders.middleware.CorsMiddleware', # Посредник для того чтобы работал corsgeaders (смотреть installed apps)
    'django.middleware.common.CommonMiddleware', # учавствует в предварительной обработке запросов (перед контроллером)
    'django.middleware.csrf.CsrfViewMiddleware', # осуществляет защиту от межсайтовых запросов 
    'django.contrib.auth.middleware.AuthenticationMiddleware', # хранит текущего пользователя и позволяет выяснить какой пользователь выполнил вход и выполнил ли он его вообще (используется администратором и разраничением доступа)
    'django.contrib.messages.middleware.MessageMiddleware', # обеспечивает работу всплывающих сообщений на низком уровне
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # реализует дополнительную защиту сайт от сетевых атак
]
'''
LOGGING = { #Вот так выглядит словарь с параметрами откладчиков 
	'version' : 1 # Выбираем версию откладчика (пока что только версия 1)
	'disable_existing_loggers' : True # Выключаем все откладчики , которые стоят по умолчанию

	'formatters' : { #Тут все форматировщики
		'simple' : { #Тут форматировщик simple 
			'format' : '[%(asctime)s] %(levelname)s: %(message)s', #формат в котором будут выводится сообщения
			'datefmt': '%Y.%m.%d %H:%M:%S',},}, #формат в которому будут выводиться время в сообщении
	
	'filters' : { #Это наши фильтры 
		'require_debug_false' : { # Это фильтр который говорит, что сообщения будут выводитья только тогда когда сайт уже находится в сети
			'()':'django.utils.log.RequireDebugFalse'},

		'require_debug_true' : { # Этот фильтр противоположен прошлому
			'()' : 'django.utils.log.RequireDebugTrue'},},

	'handlers' : { # Тут у нас обработчики 
		'console' : { #Название нашего обработчика 
			'class' : 'logging.StreamHandler', #Имя обработчика который будет выполнят вывод сообщения (в данном слвуучае в коносль)
			'level' : 'ERROR', # Минимальный уровень сообщения
			'formatter' : 'simple', # Форматер для вывода сообщения
			'filters' : ['require_debug_true'],},},	# Фильтры через которые будет проходить сообщение

	'loggers' : { # Тут у нас регистраторы 
		'django' : { # Класс регистратора (регистратор DJANGO уневирсальный (собирает все сообщения))
			'handlers' : ['console',],},}, # Обработчики нашего регистратора 
		
}
'''

ROOT_URLCONF = 'simple.urls'
# путь к модулю в котором маршруты на уровне проекта

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
                'social_django.context_processors.backends', #Это и ниже строчка для авторизации на сайте с помощью вк
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'simple.wsgi.application'

# Базы данных
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = { # Базы данных ( по умолчанию sqlite3)
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Показывает какая база данных используется в проекте (по умолчанию это SQLite) но если изменить последнее слво на postgresql, то будет использовтаться она
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), # Путь к файлу базы данных
    }
}


# Валидация поролей (валидация это проверка на корректность)
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [ # Это валидаторы, которые исползются только на страницах входа на сайт
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # сравнивает пароль с другими полями и если уровень схожетси больше 0.7 процентов то возбуждает исключение
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # Минимальное значение символов в пароле 
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # проверяет не входит ли пароль в пересень наиболее популярных паролей (есть стандартный список в котором более 1000 паролей)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # прверяет не содежрижт ли пароль одни цифры
    },
]


# Интернационализация
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru' # Языковой код, по умолчанию английский, мо можно сменить на русский

TIME_ZONE = 'Europe/Moscow' # Часовой пояс, по умолчанию UTС, но можно сменить на москву

USE_I18N = True # если включенно, то административный сайт будет автоматически переводить слова на язык указанный выше, есл нет, то не будет

USE_L10N = True # если включенно, то числа даты будут выводиться по правилам языка указанного выше, если нет, то по правилам проекта

USE_TZ = True # если включенно, то база будет хранить дату и вермя с указанием временной зоны, если нет, то временную зону для них укажет параметр time_zone


#Статичные файлы (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

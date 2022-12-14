"""
Django settings for order project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e68mz%$3fz&e$=6ngy2g83&gzny%xsg*(gh4(ls#vmvu7wy%!%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'web.apps.WebConfig',
]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'web.middleware.account.AuthMiddleware'
]

ROOT_URLCONF = 'order.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                # 'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'order.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'order',
        'USER': 'order',
        'PASSWORD': 'HALwLVV5XgxpdnGneruDKoMv',
        'HOST': '10.0.71.97',
        'PORT': 3306
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://10.0.71.98:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
            'PASSWORD': 'AtT85dywuetEAv9jCG2n5pIs',
        }
    }
}


# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

SESSION_COOKIE_NAME = 'sessionid'                 # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串
SESSION_COOKIE_PATH = '/'                         # Session的cookie保存的路径
SESSION_COOKIE_DOMAIN = None                      # Session的cookie保存的域名
SESSION_COOKIE_SECURE = False                     # 是否Https传输cookie
SESSION_COOKIE_HTTPONLY = True                    # 是否Session的cookie只支持http传输
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7             # Session的cookie失效日期（1周）

SESSION_EXPIRE_AT_BROWSER_CLOSE = False           # 是否关闭浏览器使得Session过期
SESSION_SAVE_EVERY_REQUEST = True                 # 是否每次请求都保存Session，默认修改之后才保存


# #################### Personal custom configuration ####################
# Session key
MY_SESSION_KEY = 'user_info'

# Url location
MY_LOGIN_HOME = '/home/'
MY_LOGIN_URL = '/login/'
MY_WHITE_URL = [
    '/login/',
    '/sms/login/',
    '/sms/send/',
]

# menu
MY_MENU = {
    'admin': [
        {
            'text': '用户管理',
            'icon': 'fa-bed',
            'children': [
                {'text': '级别管理', 'url': '/level/list/', 'name': 'level_list'},
                {'text': '客户管理', 'url': '/customer/list/', 'name': 'customer_list'},
            ]
        },
    ],
    'customer': [
        {
            'text': '用户信息',
            'icon': 'fa-bed',
            'children': [
            ]
        },
    ],
}

# Public
MY_PERMISSION_PUBLIC = {
    'home': {'text': '主页', 'parent': None},
    'logout': {'text': '注销', 'parent': None},
}

# Permissions
MY_PERMISSION = {
    'admin': {
        'level_list': {'text': '级别列表', 'parent': None},
        'level_add': {'text': '新建级别', 'parent': 'level_list'},
        'level_edit': {'text': '编辑级别', 'parent': 'level_list'},
        'level_delete': {'text': '删除级别', 'parent': 'level_list'},
        'customer_list': {'text': '客户列表', 'parent': None},
        'customer_add': {'text': '新建客户', 'parent': 'customer_list'},
        'customer_edit': {'text': '编辑客户', 'parent': 'customer_list'},
        'customer_reset': {'text': '修改密码', 'parent': 'customer_list'},
        'customer_delete': {'text': '删除客户', 'parent': 'customer_list'},
    },
    'customer': {
    },
}

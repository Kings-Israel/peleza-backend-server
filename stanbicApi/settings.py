import os
from pathlib import Path
from decouple import config
# import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add .env variables anywhere before SECRET_KEY
# dotenv_file = os.path.join(BASE_DIR, ".env")
# if os.path.isfile(dotenv_file):
#     dotenv.load_dotenv(dotenv_file)

# SECRET_KEY = os.environ['SECRET_KEY']  # Instead of your actual secret key

SECRET_KEY = config('SECRET_KEY')
EXTERNAL_API_PACKAGES = [34, 40, 31, 37, 41]
ALL_API_PACKAGES = list(set(EXTERNAL_API_PACKAGES + [35, 36, 38, 39, 33]))

DEBUG = True
# <<<<<<< HEAD
ALLOWED_HOSTS = ["kyc.pidva.africa","localhost", "localhost:3001", "192.168.*", "pidva.africa", "localhost:3000", "127.0.0.1","stanbic.pidva.africa", "172.105.95.169"]
# >>>>>>> 8af93b58f147af44c8cf5c007f007711ab1c379b

AUTH_USER_MODEL = "authentication.PelClient"
CORS_ALLOW_ALL_ORIGINS = True


EMAIL_HOST = config("EMAIL_HOST", None)
EMAIL_PORT = config("EMAIL_PORT", 465)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", None)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", True)
DEFAULT_FROM_EMAIL = "Peleza International"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#  File upload configuration
UPLOAD_ROOT = os.path.join(BASE_DIR,'upload')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
    "authentication",
    "debug_toolbar",
    "rest_framework",
    "import_export",
    "django_extensions",
]
INTERNAL_IPS = ["127.0.0.1", "localhost", "192.168.1.210", "172.105.95.169"]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "django.middleware.cache.UpdateCacheMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "stanbicApi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "stanbicApi.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": config("DB_NAME", "peleza_db_local"),
    #     "USER": config("DB_USER", "root"),
    #     "PASSWORD": config("DB_PASSWORD", "secretpassword"),
    #     "PORT": config("DB_PORT", 3306),
    #     "HOST": config("DB_HOST", "localhost"),
    #     "OPTIONS": {
    #         "init_command": "SET GLOBAL max_connections = 100000; ALTER DATABASE peleza_db_local CHARACTER SET utf8 "
    #                         "COLLATE utf8_general_ci;",
    #     },
    # }
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_NAME", "peleza_db_local"),
        "USER": config("DB_USER", "root"),
        "PASSWORD": config("DB_PASSWORD", "p3l3z@1234"),
        "PORT": config("DB_PORT", 3306),
        "HOST": config("DB_HOST", "46.101.16.235"),
        "OPTIONS": {
            "init_command": "SET GLOBAL max_connections = 100000; ALTER DATABASE peleza_db_local CHARACTER SET utf8 "
                            "COLLATE utf8_general_ci;",
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "authentication.authentication.ClientAuthentication",
    ),
    "DATETIME_FORMAT": "%d %b %Y %H:%M",
    "DEFAULT_PAGINATION_CLASS": "main.pagination.Pagination",
    "PAGE_SIZE": 33,
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
        "TIMEOUT": 30,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"
USE_TZ = TIME_ZONE

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

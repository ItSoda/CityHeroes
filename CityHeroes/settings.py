import os
from datetime import timedelta
from pathlib import Path

from decouple import Config, RepositoryEnv

docker = os.environ.get("DOCKER_CONTAINER")
test = os.environ.get("REDIS_TEST")
env_file = ".env"

if docker:
    env_file = "docker-compose.env"

if test:
    env_file = "test.env"

config = Config(RepositoryEnv(env_file))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get("DEBUG", default=True)

DOMAIN_NAME = config.get("DOMAIN_NAME")

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "djoser",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "corsheaders",
    "channels",
    "celery",
    "animals",
    "users",
    "tg_bot",
    "chat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "CityHeroes.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "CityHeroes.wsgi.application"

# Channels
ASGI_APPLICATION = "CityHeroes.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", "6379")],
        },
    },
}

# PARAMETRS FOR DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config.get("MYSQL_DATABASE", default="CityHeroes"),
        "USER": config.get("MYSQL_ROOT_USER", default="root"),
        "PASSWORD": config.get("MYSQL_ROOT_PASSWORD", default="nik140406"),
        "HOST": config.get("MYSQL_HOST", default="localhost"),
        "PORT": config.get("MYSQL_PORT", default="3306"),
    }
}


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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
if docker:
    STATIC_ROOT = "static"
else:
    STATICFILES_DIRS = [BASE_DIR / "static"]

# Base url to serve media files
MEDIA_URL = "/media/"
# Path where media is stored
MEDIA_ROOT = "media"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# User
AUTH_USER_MODEL = "users.Users"

# Redis
REDIS_HOST = config.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = 6379
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


# Djoser
DJOSER = {
    "PERMISSIONS": {
        "user_list": ["rest_framework.permissions.IsAdminUser"],
        "password_reset": ["rest_framework.permissions.AllowAny"],
        "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "set_password": ["rest_framework.permissions.AllowAny"],
    },
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {
        "user_create": "users.serializers.UserRegistSerializer",
        "current_user": "users.serializers.UserProfile",
    },
}

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5000),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# Email
EMAIL_HOST = config.get("EMAIL_HOST")
EMAIL_HOST_USER = config.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = config.get("EMAIL_USE_SSL")
EMAIL_PORT = config.get("EMAIL_PORT")
DEFAULT_FROM_EMAIL = config.get("DEFAULT_FROM_EMAIL")


# CSRF
CSRF_TRUSTED_ORIGINS = ["https://boar-still-alpaca.ngrok-free.app", "http://red-store.site", "https://red-store.site"]


# yookassa
YOOKASSA_REDIRECT_URL = "/admin/"
YOOKASSA_SHOP_ID = config.get("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = config.get("YOOKASSA_SECRET_KEY")


# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:50000",
    "http://localhost:3000",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_URLS_REGEX = r"^/.*$"


# TELEGRAM BOT
TELEGRAM_BOT_TOKEN = config.get("TELEGRAM_BOT_TOKEN")
ADMIN_ID = config.get("ADMIN_ID")

# DEBUG TOOLBAR

INTERNAL_IPS = [
    "127.0.0.1",
]

REDIS_HOST = config.get("REDIS_HOST", "localhost")

# CELERY
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
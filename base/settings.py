import os
from pathlib import Path

import environ

env = environ.Env()


BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]


# DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# Application definition

INSTALLED_APPS = [
    # default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # email verification
    "django_email_verification",
    # allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    # restframework
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "django_filters",
    # crispy
    "crispy_forms",
    "crispy_bootstrap5",
    # my_apps
    "src.applications.books",
    "src.rest.books_api",
    "src.applications.users",
    "src.rest.users_api",
    "src.applications.book_relations",
    "src.rest.book_relations_api",
    "src.applications.book_requests",
    "src.rest.book_requests_api",
    "src.applications.chat",
    "src.rest.chat_api",
    "src.applications.gallery",
    "src.applications.news",
    "src.rest.news_api",
    "src.applications.subscriptions",
    "src.rest.subscriptions_api",
    # other
    "phonenumber_field",
    "django_countries",
    "debug_toolbar",
    "django.contrib.humanize",
    "captcha",
    "taggit",
    "django_celery_beat",
    "django_celery_results",
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Debug toolbar
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # user activity
    "src.applications.users.middleware.UserActivityMiddleware",
    # allauth
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "base.urls"

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

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
                "src.applications.book_requests.context_processors.total_requests",
            ],
        },
    },
]

# Crispy templates

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


WSGI_APPLICATION = "base.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

# FOR DOCKER
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
    },
    "test": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME_TEST", "test_" + os.environ.get("DB_NAME", "")),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
    },
}
# Local DB

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "bookchange_db",
#         "USER": "postgres",
#         "PASSWORD": "",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }


FIXTURE_DIRS = [BASE_DIR / "fixtures"]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "static"]


MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Users

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "users:login"

LOGIN_REDIRECT_URL = "books:index"

LOGOUT_REDIRECT_URL = "books:index"


# Allauth
ACCOUNT_USER_MODEL = "users.User"


ACCOUNT_AUTHENTICATION_METHOD = "email"
CCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "SCOPE": [
            "user",
            "repo",
            "read:org",
        ],
    }
}


SIDE_ID = 1

# Email verification


def email_verified_callback(user):
    user.is_active = True


# Global Package Settings
EMAIL_FROM_ADDRESS = env("EMAIL_FROM_USER")  # mandatory
EMAIL_PAGE_DOMAIN = "http://127.0.0.1:8000/"  # mandatory (unless you use a custom link)
EMAIL_MULTI_USER = False  # optional (defaults to False)

# Email Verification Settings (mandatory for email sending)
EMAIL_MAIL_SUBJECT = "Confirm your email {{ user.username }}"
EMAIL_MAIL_HTML = "users/register/mail_body.html"
EMAIL_MAIL_PLAIN = "users/register/mail_body.txt"
EMAIL_MAIL_TOKEN_LIFE = 60 * 60  # one hour

# Email Verification Settings (mandatory for builtin view)
EMAIL_MAIL_PAGE_TEMPLATE = "users/register/email-verification-success.html"
EMAIL_MAIL_CALLBACK = email_verified_callback


# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "sergiy06061997@gmail.com"
EMAIL_HOST_PASSWORD = "rxhuparrjvmafsud"  # os.environ['password_key'] suggested
EMAIL_USE_TLS = True

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# rest framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    # ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 5,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
}


# Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

SESSION_COOKIE_AGE = 12000
SESSION_SAVE_EVERY_REQUEST = True


REDIS_HOST = "redis"
REDIS_PORT = "6379"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
    }
}


# Celery

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BASKEND = "redis://redis:6379/0"
CELERY_broker_connection_retry_on_startup = True

broker_connection_retry_on_startup = False
# Crontab


# Stripe

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")

STRIPE_VERSION = env("STRIPE_VERSION")

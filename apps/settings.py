import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

ENVIRONMENT_DEV = "DEV"
ENVIRONMENT_PROD = "PROD"
ENVIRONMENT = os.environ.get("ENVIRONMENT", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

if ENVIRONMENT == ENVIRONMENT_DEV:
    ALLOWED_HOSTS = ["*"]
elif ENVIRONMENT == ENVIRONMENT_PROD:
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        ".herokuapp.com",
    ]
else:
    raise ValueError("Unknown environment")

# HEROKU_APP_DEFAULT_DOMAIN_NAME = os.environ.get("HEROKU_APP_DEFAULT_DOMAIN_NAME")
# if HEROKU_APP_DEFAULT_DOMAIN_NAME:
#    ALLOWED_HOSTS.append(f"HEROKU_APP_DEFAULT_DOMAIN_NAME")

if ENVIRONMENT == ENVIRONMENT_DEV:
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:8088",
        "http://localhost:3000",
        "http://0.0.0.0:8088",
        "http://0.0.0.0:3000",
        "http://127.0.0.1:8088",
        "http://127.0.0.1:3000",
    ]

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8088",
        "http://localhost:3000",
        "http://0.0.0.0:8088",
        "http://0.0.0.0:3000",
        "http://127.0.0.1:8088",
        "http://127.0.0.1:3000",
    ]
elif ENVIRONMENT == ENVIRONMENT_PROD:
    CSRF_TRUSTED_ORIGINS = [
        "https://pet-hotel-frontend-456dd50e3c69.herokuapp.com",
        "https://pet-hotel-074de305ca4c.herokuapp.com",
    ]

    CORS_ALLOWED_ORIGINS = [
        "https://pet-hotel-frontend-456dd50e3c69.herokuapp.com",
        "https://pet-hotel-074de305ca4c.herokuapp.com",
    ]
else:
    raise ValueError("Unknown environment")

if ENVIRONMENT == ENVIRONMENT_PROD:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https://pet\-hotel\-.*\.herokuapp\.com$",
    ]

if ENVIRONMENT == ENVIRONMENT_DEV:
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    CSRF_COOKIE_SAMESITE = "Lax"
elif ENVIRONMENT == ENVIRONMENT_PROD:
    # Force cookies to be sent over HTTPS only (Required for SameSite=None)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Allow cookies to be sent in cross-site requests
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"

    # Ensure cookies are protected from client-side scripts
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
else:
    raise ValueError("Unknown environment")

CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "apps.embassy",
    "apps.mail",
    "apps.hotel",
    "apps.auth",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "apps.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "apps.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASE_URL = os.environ.get("DATABASE_URL")

DATABASES = {
    "default": {
        **dj_database_url.config(default=DATABASE_URL),
        "DISABLE_SERVER_SIDE_CURSORS": True,
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("es", "Español"),
    ("en", "English"),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

LOCALE_PATHS = [
    BASE_DIR / "apps" / "embassy" / "locale",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

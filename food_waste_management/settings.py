import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# =========================
# SECRET KEY
# =========================

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "unsafe-development-key"
)


# =========================
# DEBUG
# =========================

DEBUG = os.getenv(
    "DJANGO_DEBUG",
    "True"
).lower() == "true"


# =========================
# ALLOWED HOSTS
# =========================

ALLOWED_HOSTS = ["*"]


# =========================
# INSTALLED APPS
# =========================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",

    "users",
    "food",
    "donation",
    "analytics",
]


# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================
# URL CONFIGURATION
# =========================

ROOT_URLCONF = "food_waste_management.urls"


# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


# =========================
# WSGI
# =========================

WSGI_APPLICATION = "food_waste_management.wsgi.application"


# =========================
# DATABASE - MYSQL
# =========================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",

        "NAME": os.getenv(
            "MYSQL_DATABASE"
        ),

        "USER": os.getenv(
            "MYSQL_USER"
        ),

        "PASSWORD": os.getenv(
            "MYSQL_PASSWORD"
        ),

        "HOST": os.getenv(
            "MYSQL_HOST"
        ),

        "PORT": os.getenv(
            "MYSQL_PORT"
        ),
    }
}


# =========================
# CUSTOM USER MODEL
# =========================

AUTH_USER_MODEL = "users.User"


# =========================
# LANGUAGE / TIMEZONE
# =========================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# =========================
# STATIC FILES
# =========================

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================
# DEFAULT PRIMARY KEY
# =========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================
# LOGIN
# =========================

LOGIN_URL = "/login/"


# =========================
# DJANGO REST FRAMEWORK
# =========================

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],

    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication"
    ]
}


# =========================
# MONGODB
# =========================

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://127.0.0.1:27017/"
)

MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "food_waste_history"
)
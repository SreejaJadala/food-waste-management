import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-development-key")

DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS=[]
INSTALLED_APPS=[
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
    "analytics"
]
MIDDLEWARE=\
    ["django.middleware.security.SecurityMiddleware",
     "django.contrib.sessions.middleware.SessionMiddleware",
     "django.middleware.common.CommonMiddleware",
     "django.middleware.csrf.CsrfViewMiddleware",
     "django.contrib.auth.middleware.AuthenticationMiddleware",
     "django.contrib.messages.middleware.MessageMiddleware",
     "django.middleware.clickjacking.XFrameOptionsMiddleware"
     ]
ROOT_URLCONF="food_waste_management.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR / "templates"],
            "APP_DIRS":True,
            "OPTIONS":{"context_processors":["django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="food_waste_management.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_HOST"),
        "PORT": os.getenv("MYSQL_PORT"),
    }
}


AUTH_USER_MODEL="users.User"
LANGUAGE_CODE="en-us"
TIME_ZONE="Asia/Kolkata"
USE_I18N=True
USE_TZ=True
STATIC_URL="static/"
STATICFILES_DIRS=[BASE_DIR / "static"]
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
LOGIN_URL="/login/"
REST_FRAMEWORK={
    "DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES":["rest_framework.authentication.SessionAuthentication"]
}
MONGODB_URI=os.getenv("MONGODB_URI","mongodb://127.0.0.1:27017/")
MONGODB_DATABASE=os.getenv("MONGODB_DATABASE","food_waste_history")

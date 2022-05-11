
from pathlib import Path
import os
from dotenv import load_dotenv

# ...
try:
    from config.settings_local import DEBUG, DATABASES, ALLOWED_HOSTS
except ImportError:
    from config.host_settings import DEBUG, DATABASES, ALLOWED_HOSTS


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# ...
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

load_dotenv(dotenv_path=os.getenv("dotenv_path"))
SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS_SWITCHING = ALLOWED_HOSTS
DEBUG_SWITCHING = DEBUG

SITE_ID = 3
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static/"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

DISABLE_COLLECTSTATIC = 1

LOGIN_REDIRECT_URL = "/profile/"
LOGIN_URL = "login"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_filters",
    "sorl.thumbnail",
    "widget_tweaks",
    "crispy_forms",
    "secretballot",
    "sortedm2m",
    "likes",
    "star_ratings",
    "import_export",
    "cuser",
    "taggit",
    "event",
    "main",
    "restcomplex",
    "client",
    "agent",
    "sendemail",
    "payments",
    "search",
    "overview_correction",
    "ckeditor",
    "ckeditor_uploader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "secretballot.middleware.SecretBallotIpUseragentMiddleware",
    "likes.middleware.SecretBallotUserIpUseragentMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


LANGUAGE_CODE = "en"
# TIME_ZONE = "Europe/Minsk"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ...
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = "587"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
MANAGERS = (("Siarhei Bloggs", os.getenv("EMAIL_HOST_USER")),)
EMAIL_SUBJECT_PREFIX = "[Oscar myshop]"


# ...
SECRETBALLOT_FOR_MODELS = {
    "restcomplex.RestOffersFor": {},
}

# ...
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

CRISPY_TEMPLATE_PACK = "uni_form"

CKEDITOR_JQUERY_URL = "https://code.jquery.com/jquery-3.6.0.min.js"
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "default": {"removePlugins": "stylesheetparser", "allowedContent": True,}
}
IMPORT_EXPORT_USE_TRANSACTIONS = True

# ...
DATABASES_SWITCHING = DATABASES


import django_heroku
import dj_database_url

django_heroku.settings(locals())
DATABASES["default"] = dj_database_url.config(
    conn_max_age=600,
    ssl_require=True,
    default=os.getenv("POSTGRESQL_URI"),
)

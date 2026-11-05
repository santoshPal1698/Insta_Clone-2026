
import os
from django.contrib.messages import constants as messages
from pathlib import Path
from dotenv import load_dotenv
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is required")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# =========================================================
# SECURITY SETTINGS
# =========================================================


ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS", ""
    ).split(",")
    if origin.strip()
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / os.getenv("DB_NAME", "db.sqlite3"),
    }
}



# =========================================================
# INSTALLED APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    "unfold",
    # Django default applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Project applications
    "social",
    # Third-party applications
    "cloudinary_storage",
    "cloudinary",
    "crispy_forms",
    "crispy_bootstrap4",
]


# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# =========================================================
# MIDDLEWARE
# =========================================================

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


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = "instapro.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
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


# =========================================================
# WSGI CONFIGURATION
# =========================================================

WSGI_APPLICATION = "instapro.wsgi.application"


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# =========================================================
# PASSWORD VALIDATION
# =========================================================

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


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILE CONFIGURATION
# =========================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]


STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND":  "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


if os.getenv("CLOUDINARY_URL"):
    CLOUDINARY_STORAGE = {}
else:
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
        "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
        "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    }

# =========================================================
# MEDIA FILE CONFIGURATION
# =========================================================

# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# =========================================================
# DEFAULT IMAGE FIELD CONFIGURATION
# =========================================================

DEFAULT_IMAGE_PATH = "static/django_fields/no_image.png"

# =========================================================
# CRISPY FORMS CONFIGURATION
# =========================================================

CRISPY_TEMPLATE_PACK = "bootstrap4"

# =========================================================
# EMAIL CONFIGURATION
# =========================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# =========================================================
# LOGIN CONFIGURATION
# =========================================================

LOGIN_REDIRECT_URL = "/"


# =========================================================
# DJANGO MESSAGES
# =========================================================

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"



# =========================================================
# UNFOLD ADMIN CONFIGURATION
# =========================================================

UNFOLD = {
    "SITE_TITLE": "SP-INSTA Admin",
    "SITE_HEADER": "SP-INSTA",
    "SITE_SUBHEADER": "Social platform management",
    "SITE_URL": "/",
    "SITE_SYMBOL": "dashboard",
    "DASHBOARD_CALLBACK": "social.admin.dashboard_callback",

    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "COMMAND": {
        "search_models": True,
        "show_history": True,
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Overview"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Social"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Posts"),
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:social_mypost_changelist"),
                    },
                    {
                        "title": _("Profiles"),
                        "icon": "group",
                        "link": reverse_lazy("admin:social_myprofile_changelist"),
                    },
                    {
                        "title": _("Comments"),
                        "icon": "chat",
                        "link": reverse_lazy("admin:social_comment_changelist"),
                    },
                    {
                        "title": _("Follows"),
                        "icon": "person_add",
                        "link": reverse_lazy("admin:social_followuser_changelist"),
                    },
                    {
                        "title": _("Likes"),
                        "icon": "favorite",
                        "link": reverse_lazy("admin:social_postlike_changelist"),
                    },
                    {
                        "title": _("Contact messages"),
                        "icon": "mail",
                        "link": reverse_lazy("admin:social_contact_changelist"),
                    },
                ],
            },
        ],
    },

    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "29 78 216",
            "800": "30 64 175",
            "900": "30 58 138",
            "950": "23 37 84",
        },
    },
}

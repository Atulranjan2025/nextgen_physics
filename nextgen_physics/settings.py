"""
✅ Django settings for nextgen_physics project
Automatically detects local vs production using manage_env.py
Compatible with Render.com and local development
"""

import os
from pathlib import Path
import dj_database_url
from nextgen_physics.manage_env import setup_environment  # ✅ Auto environment loader

# ==================== LOAD ENVIRONMENT ====================
setup_environment()  # Automatically loads .env.local or .env.production

# ==================== BASE CONFIG ====================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== SECURITY SETTINGS ====================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,nextgenphysics.in,www.nextgenphysics.in,.onrender.com"
).split(",")

# ==================== APPLICATIONS ====================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notes.apps.NotesConfig',
    'django_extensions',
    'cloudinary',
    'cloudinary_storage',
    'ai_notes',
]


# ==================== CLOUDINARY CONFIGURATION ====================

CLOUDINARY_STORAGE = {
    
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME', 'dj8hliupo'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', '531811533591827'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', 'v0p2nnTjDIwgXqw2LdTDwrMggSc'),
}

# ==================== DEFAULT FILE STORAGE (Auto switch) ====================

if DEBUG:
    # ✅ Local development: store files in /media/
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    # ✅ Production (Render): store files on Cloudinary
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ==================== MIDDLEWARE ====================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # static files handler for Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'nextgen_physics.middleware.ForceSecureCookiesMiddleware',  # ✅ Secure cookie middleware
]

ROOT_URLCONF = 'nextgen_physics.urls'

# ==================== TEMPLATES ====================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nextgen_physics.wsgi.application'

# ==================== DATABASE ====================

DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL.startswith("postgresql://"):
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ==================== PASSWORD VALIDATION ====================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==================== LANGUAGE & TIMEZONE ====================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ==================== STATIC & MEDIA ====================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==================== COOKIE / SECURITY SETTINGS ====================

MODE = os.getenv("MODE", "local").strip().lower()

if MODE == "production":
    # ✅ Production (Render)
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # ✅ Local
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0

# ✅ CSRF and Session Settings
CSRF_TRUSTED_ORIGINS = [
    "https://nextgenphysics.in",
    "https://www.nextgenphysics.in",
    "https://nextgenphysics.onrender.com",
]

SESSION_COOKIE_SAMESITE = "None" if MODE == "production" else "Lax"
CSRF_COOKIE_SAMESITE = "None" if MODE == "production" else "Lax"

SESSION_COOKIE_DOMAIN = ".nextgenphysics.in" if MODE == "production" else None
CSRF_COOKIE_DOMAIN = ".nextgenphysics.in" if MODE == "production" else None

# ==================== DEFAULT AUTO FIELD ====================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== DEBUG LOGS ====================

print(f"✅ Mode: {MODE}")
print(f"✅ Using Database: {'PostgreSQL' if DATABASE_URL.startswith('postgresql://') else 'SQLite'}")
print(f"✅ Debug Mode: {DEBUG}")
print(f"✅ Allowed Hosts: {ALLOWED_HOSTS}")
print(f"✅ Storage: {'Cloudinary' if not DEBUG else 'Local /media/'}")
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("AIzaSyDzwvHrENi0iegMKCZkg9Squ0e9Y2yN334")

# -------------------- Default Primary Key --------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


   
   
   
 
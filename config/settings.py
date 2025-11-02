import dj_database_url
from decouple import config
import os

"""
Django settings for budget tracker project.
This file controls all configuration for the Django application.
"""

from pathlib import Path
from decouple import config

# Build paths inside the project
# BASE_DIR points to the root directory of your project
# Example: /home/user/budget-tracker-backend/
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY is used for cryptographic signing (sessions, tokens, etc.)
# In production, this should be stored in environment variables
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True shows detailed error pages (helpful for development)
# DEBUG = False shows generic error pages (required for production)
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS - Allow Railway domain
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', 
    default='127.0.0.1,localhost,budgettracker-production-033c.up.railway.app',
    cast=lambda v: [s.strip() for s in v.split(',')]
)


# Application definition
# INSTALLED_APPS: All Django apps that are active in this project
INSTALLED_APPS = [
    # Django built-in apps (admin interface, authentication, etc.)
    'django.contrib.admin',        # Admin panel at /admin
    'django.contrib.auth',         # User authentication system
    'django.contrib.contenttypes', # Content type system
    'django.contrib.sessions',     # Session management
    'django.contrib.messages',     # Messaging framework
    'django.contrib.staticfiles',  # Static files (CSS, JS, images)
    
    # Third-party apps
    'rest_framework',              # Django REST Framework for APIs
    'rest_framework.authtoken',    # Token authentication
    'corsheaders',                 # CORS headers for frontend communication
    'django_filters',              # Filtering support for APIs
    
    # Our custom apps
    'apps.users',                  # User authentication app
    'apps.transactions',           # Transaction management app
    'apps.categories',             # Category management app
    'apps.budgets',                # Budget management app

    'django_extensions',
]

# MIDDLEWARE: Functions that process requests/responses
# Order matters! Each middleware wraps the next one
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',     # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'corsheaders.middleware.CorsMiddleware',             # CORS handling (must be before CommonMiddleware)
    'django.middleware.common.CommonMiddleware',         # Common utilities
    'django.middleware.csrf.CsrfViewMiddleware',         # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',     # Messages framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Clickjacking protection
]

# Root URL configuration
# This points to the main urls.py file
ROOT_URLCONF = 'config.urls'

# Templates configuration (we won't use templates as we're building an API)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI application (for deployment)
WSGI_APPLICATION = 'config.wsgi.application'


# Database configuration
# Using SQLite for development (file-based database)
# In production, switch to PostgreSQL or MySQL
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# # Database - Use PostgreSQL in production
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('PGDATABASE', default='railway'),
#         'USER': config('PGUSER', default='postgres'),
#         'PASSWORD': config('PGPASSWORD', default=''),
#         'HOST': config('PGHOST', default='localhost'),
#         'PORT': config('PGPORT', default='5432'),
#     }
# }


# Password validation
# Django enforces these rules when users create passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # Prevents passwords similar to user attributes (username, email)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Enforces minimum password length (default: 8 characters)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # Prevents common passwords like "password123"
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Prevents purely numeric passwords
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'      # Default language
TIME_ZONE = 'Asia/Kolkata'   # Your timezone (changed to IST)
USE_I18N = True              # Enable internationalization
USE_TZ = True                # Use timezone-aware datetimes


# Static files (CSS, JavaScript, Images)
# These settings tell Django where to find and serve static files
# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# Determines the type of auto-generated ID fields
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST Framework Configuration
# This configures how Django REST Framework behaves
REST_FRAMEWORK = {
    # Default authentication classes
    # TokenAuthentication: Uses token-based authentication (we'll use this)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    
    # Default permission classes
    # IsAuthenticated: Only authenticated users can access APIs
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # Pagination settings
    # Limits number of results returned per API call
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # 10 items per page
    
    # Filter backend
    # Allows filtering, searching, and ordering of querysets
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
    # Response format
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',      # JSON responses
        'rest_framework.renderers.BrowsableAPIRenderer',  # Web UI for testing APIs
    ],
}


# CORS Configuration
# CORS (Cross-Origin Resource Sharing) allows React app to communicate with Django

# For development: Allow all origins
# CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)

# For production: Specify exact origins
# CORS_ALLOWED_ORIGINS = [
#     "https://your-frontend-domain.com",
# ]


# CORS Configuration - Update for your Railway URL
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)

# For production, use specific origins
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='',
    cast=lambda v: [s.strip() for s in v.split(',')] if v else []
)

# If no specific origins provided and not allowing all, allow localhost for testing
if not CORS_ALLOW_ALL_ORIGINS and not CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']

# Allow credentials (cookies, authorization headers)
CORS_ALLOW_CREDENTIALS = True

# Headers that browser can access
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# HTTP methods allowed
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
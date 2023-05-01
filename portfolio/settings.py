from pathlib import Path
from datetime import timedelta
import os
import sys
# from decouple import config
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default=1)))

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(" "),
    ))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'ckeditor',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'accounts',
    'cart',
    'core',
    'product',
    'orders',
    'social_posts',
    'social_profiles',
]

CORS_ALLOWED_ORIGINS = []
CORS_ALLOWED_ORIGINS.extend(
    filter(
        None,
        os.environ.get('CORS_ALLOWED_ORIGINS', '').split(" "),
    ))

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'portfolio/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.menu_categories',
                'core.context_processors.core_tags',
                'product.context_processors.menu_categories',
                'product.context_processors.top_categories',
                'cart.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'

DATABASES = {
    "default": {
        "ENGINE":
        os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME":
        os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER":
        os.environ.get("SQL_USER", "user"),
        "PASSWORD":
        os.environ.get("SQL_PASSWORD", "password"),
        "HOST":
        os.environ.get("SQL_HOST", "localhost"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'
STATICFILES_DIRS = []

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    "127.0.0.1",
]

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# SMTP configuration
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")

CKEDITOR_UPLOAD_PATH = "uploads/"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}
DJOSER = {
    'ACTIVATION_URL': 'accounts/activate/{uid}/{token}/',
    'SEND_ACTIVATION_EMAIL': True,
    'USER_ACTIVATION': {
        'SEND_EMAIL': True,
        'ACTIVATION_AFTER_REGISTRATION': True,
        'SEND_CONFIRMATION_EMAIL': True,
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":
    timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME":
    timedelta(days=1),
    "ROTATE_REFRESH_TOKENS":
    False,
    "BLACKLIST_AFTER_ROTATION":
    False,
    "UPDATE_LAST_LOGIN":
    False,
    "ALGORITHM":
    "HS256",
    "SIGNING_KEY":
    SECRET_KEY,
    "VERIFYING_KEY":
    "",
    "AUDIENCE":
    None,
    "ISSUER":
    None,
    "JSON_ENCODER":
    None,
    "JWK_URL":
    None,
    "LEEWAY":
    0,
    "AUTH_HEADER_TYPES": ("Bearer", ),
    "AUTH_HEADER_NAME":
    "HTTP_AUTHORIZATION",
    "USER_ID_FIELD":
    "id",
    "USER_ID_CLAIM":
    "user_id",
    "USER_AUTHENTICATION_RULE":
    "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken", ),
    "TOKEN_TYPE_CLAIM":
    "token_type",
    "TOKEN_USER_CLASS":
    "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM":
    "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM":
    "refresh_exp",
    "SLIDING_TOKEN_LIFETIME":
    timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME":
    timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER":
    "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER":
    "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER":
    "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER":
    "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER":
    "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER":
    "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

CKEDITOR_CONFIGS = {
    'default': {
        'skin':
        'moono-lisa',
        # 'skin': 'office2013',
        'toolbar_Basic': [['Source', '-', 'Bold', 'Italic']],
        'toolbar_YourCustomToolbarConfig': [
            {
                'name':
                'document',
                'items': [
                    'Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-',
                    'Templates'
                ]
            },
            {
                'name':
                'clipboard',
                'items': [
                    'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-',
                    'Undo', 'Redo'
                ]
            },
            {
                'name': 'editing',
                'items': ['Find', 'Replace', '-', 'SelectAll']
            },
            {
                'name':
                'forms',
                'items': [
                    'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea',
                    'Select', 'Button', 'ImageButton', 'HiddenField'
                ]
            },
            '/',
            {
                'name':
                'basicstyles',
                'items': [
                    'Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                    'Superscript', '-', 'RemoveFormat'
                ]
            },
            {
                'name':
                'paragraph',
                'items': [
                    'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
                    '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft',
                    'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-',
                    'BidiLtr', 'BidiRtl', 'Language'
                ]
            },
            {
                'name': 'links',
                'items': ['Link', 'Unlink', 'Anchor']
            },
            {
                'name':
                'insert',
                'items': [
                    'Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley',
                    'SpecialChar', 'PageBreak', 'Iframe'
                ]
            },
            '/',
            {
                'name': 'styles',
                'items': ['Styles', 'Format', 'Font', 'FontSize']
            },
            {
                'name': 'colors',
                'items': ['TextColor', 'BGColor']
            },
            {
                'name': 'tools',
                'items': ['Maximize', 'ShowBlocks']
            },
            {
                'name': 'about',
                'items': ['About']
            },
            '/',  # put this to force next toolbar on new line
            {
                'name':
                'yourcustomtools',
                'items': [
                    # put the name of your editor.ui.addButton here
                    'Preview',
                    'Maximize',
                ]
            },
        ],
        'toolbar':
        'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces':
        4,
        'extraPlugins':
        ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

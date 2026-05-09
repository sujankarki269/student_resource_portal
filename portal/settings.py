import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost,sujankarki269.com.np,www.sujankarki269.com.np', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',          # required by allauth
    'core',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',   # Google provider
    'django_ckeditor_5'
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITE_ID = config('SITE_ID', default=2, cast=int)

ROOT_URLCONF = 'portal.urls'

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

WSGI_APPLICATION = 'portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if config('USE_SQLITE', default=False, cast=bool):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static')]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allow same-origin iframes (needed for in-page PDF preview)
X_FRAME_OPTIONS = 'SAMEORIGIN'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

ACCOUNT_EMAIL_VERIFICATION = 'none'      # skip email confirmation
ACCOUNT_SIGNUP_ENABLED = False           # disable local signup (only social)
LOGIN_URL = '/accounts/login/'           # allauth's login page
LOGIN_REDIRECT_URL = '/'                  # after login, go home
LOGOUT_REDIRECT_URL = '/'          # after logout, go to home (or login page)
SOCIALACCOUNT_ONLY = True 
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

# CKEditor 5 Configuration
CKEDITOR_5_UPLOAD_PATH = "uploads/"
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', '|',
            'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', '|',
            'alignment', '|',
            'bulletedList', 'numberedList', 'todoList', '|',
            'outdent', 'indent', '|',
            'link', 'blockQuote', 'code', 'codeBlock', '|',
            'imageUpload', 'insertTable', 'mediaEmbed', 'horizontalLine', '|',
            'removeFormat', 'undo', 'redo', '|',
            'specialCharacters', 'superscript', 'subscript'
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative', '|',
                'imageStyle:alignLeft', 'imageStyle:alignCenter', 'imageStyle:alignRight'
            ],
            'styles': {
                'alignLeft': {
                    'name': 'Left aligned',
                    'icon': 'left',
                    'className': 'image-align-left'
                },
                'alignCenter': {
                    'name': 'Centered',
                    'icon': 'center',
                    'className': 'image-align-center'
                },
                'alignRight': {
                    'name': 'Right aligned',
                    'icon': 'right',
                    'className': 'image-align-right'
                },
            }
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells']
        },
        'codeBlock': {
            'languages': [
                {'language': 'plaintext', 'label': 'Plain text'},
                {'language': 'python', 'label': 'Python'},
                {'language': 'javascript', 'label': 'JavaScript'},
                {'language': 'html', 'label': 'HTML'},
                {'language': 'css', 'label': 'CSS'},
                {'language': 'bash', 'label': 'Bash/Shell'},
            ]
        },
        'height': 500,
        'width': '100%',
        'removePlugins': ['Markdown'],  # if you don't want markdown support
    },
}

# ===== JAZZMIN ADMIN THEME =====
JAZZMIN_SETTINGS = {
    "site_title": "SRP Admin",
    "site_header": "Student Resource Portal",
    "site_brand": "SRP",
    "welcome_sign": "IOE Purwanchal Campus — Admin Panel",
    "copyright": "IOE Purwanchal Campus",
    "search_model": ["core.Note", "core.Assignment", "core.Program", "core.BlogPost"],
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site",  "url": "/", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "View Site", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "core", "auth",
        "core.note", "core.assignment", "core.program",
        "core.subject", "core.tag",
        "core.category", "core.blogpost",
        "core.announcement",
        "core.bookmark", "core.tutorialprogress",
        "core.publicationcategory", "core.publicationitem",
        "core.portfolioprofile",
    ],
    "icons": {
        "auth":                     "fas fa-users-cog",
        "auth.user":                "fas fa-user",
        "auth.Group":               "fas fa-users",
        "core.Note":                "fas fa-book-open",
        "core.Assignment":          "fas fa-clipboard-list",
        "core.Program":             "fas fa-code",
        "core.Subject":             "fas fa-graduation-cap",
        "core.Tag":                 "fas fa-tag",
        "core.Category":            "fas fa-folder",
        "core.BlogPost":            "fas fa-file-alt",
        "core.Announcement":        "fas fa-bullhorn",
        "core.Bookmark":            "fas fa-bookmark",
        "core.TutorialProgress":    "fas fa-tasks",
        "core.Profile":             "fas fa-id-card",
        "core.PortfolioProfile":    "fas fa-user-tie",
        "core.PublicationCategory": "fas fa-folder-open",
        "core.PublicationItem":     "fas fa-newspaper",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "use_google_fonts_cdn": False,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-outline-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },
}

# X_FRAME_OPTIONS kept as SAMEORIGIN (needed for in-page PDF preview)
# W019 silenced intentionally
SILENCED_SYSTEM_CHECKS = ['security.W019']

# ===== PRODUCTION SECURITY =====
if not DEBUG:
    CSRF_TRUSTED_ORIGINS        = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())
    SECURE_SSL_REDIRECT         = True
    SESSION_COOKIE_SECURE       = True
    CSRF_COOKIE_SECURE          = True
    SECURE_BROWSER_XSS_FILTER   = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS         = 31536000   # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD         = True
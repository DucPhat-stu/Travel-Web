"""
Thêm vào file travel_tourism/settings.py hoặc core/settings.py
"""

# ====================
# MIDDLEWARE
# ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Thêm custom middleware
    'users.middleware.AuthMiddleware',  # Middleware phân quyền
]

# ====================
# TEMPLATES
# ====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # pyright: ignore[reportUndefinedVariable]
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # Thêm context processor
                'users.context_processors.user_context',  # User info
            ],
        },
    },
]

# ====================
# EMAIL CONFIGURATION (cho chức năng forget password)
# ====================
# Development: In email ra console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production: Dùng SMTP (Gmail, SendGrid, ...)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@travel-tourism.com'

# ====================
# SESSION CONFIGURATION
# ====================
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Lưu session vào DB
SESSION_COOKIE_AGE = 86400  # 24 giờ
SESSION_COOKIE_NAME = 'travel_sessionid'
SESSION_SAVE_EVERY_REQUEST = False

# ====================
# SECURITY
# ====================
# Development
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Production (uncomment khi deploy)
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
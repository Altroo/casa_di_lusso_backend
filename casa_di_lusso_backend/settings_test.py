from casa_di_lusso_backend.settings import *  # noqa: F401, F403

DEBUG = True
SECURE_SSL_REDIRECT = False
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]
MIDDLEWARE = [
    middleware
    for middleware in MIDDLEWARE
    if middleware != "whitenoise.middleware.WhiteNoiseMiddleware"
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

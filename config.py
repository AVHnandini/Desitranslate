# Desi Translate Configuration File

# Application Settings
APP_NAME = "Desi Translate"
APP_VERSION = "1.0.0"
DEBUG = True
SECRET_KEY = "desi_translate_secret_key_2026"

# Database Configuration
DATABASE = "users.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Translation Settings
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hindi": "Hindi (हिन्दी)",
    "spanish": "Spanish (Español)",
    "french": "French (Français)"
}

# Feature Toggles
FEATURES = {
    "text_translator": True,
    "voice_input": True,
    "voice_output": True,
    "idiom_translator": True,
    "slang_normalizer": True,
    "historical_translator": True,
    "video_translator": True,
    "user_authentication": True
}

# Voice Settings
VOICE_CONFIG = {
    "hindi": {"lang": "hi-IN", "voice": "Google हिंदी"},
    "spanish": {"lang": "es-ES", "voice": "Google Español"},
    "french": {"lang": "fr-FR", "voice": "Google Français"},
    "english": {"lang": "en-US", "voice": "Google US English"}
}

# File Upload Settings
MAX_FILE_SIZE = 5242880  # 5MB in bytes
ALLOWED_EXTENSIONS = {"srt", "vtt", "txt"}

# Server Settings
HOST = "0.0.0.0"
PORT = 5000
THREADED = True

# Session Configuration
PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
SESSION_COOKIE_SECURE = False  # Set to True in production
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "app.log"

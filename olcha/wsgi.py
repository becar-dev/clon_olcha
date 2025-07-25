import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olcha.settings')

# Standart Django application'ni olamiz
application = get_wsgi_application()

# WhiteNoise'ni application'ga o'raymiz. Endi u statik fayllarni
# samarali yetkazib bera oladi.
application = WhiteNoise(application)
from django.apps import AppConfig



class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

    def ready(self):
        # Ilova tayyor bo'lganda signallarni import qiladi
        import reviews.signals

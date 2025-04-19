# faults/apps.py
from django.apps import AppConfig

class FaultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faults'

    def ready(self):
        import faults.signals  # <-- Connects the signal


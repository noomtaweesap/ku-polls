"""Apps configuration for polls."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Polls config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

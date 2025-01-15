from __future__ import absolute_import, unicode_literals

# Stellt sicher, dass Celery beim Importieren geladen wird
from .celery import app as celery_app

__all__ = ('celery_app',)

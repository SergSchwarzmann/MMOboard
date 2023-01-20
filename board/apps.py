from django.apps import AppConfig
import os


class BoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board'

    def ready(self):
        import board.signals

        from .scheduler import board_scheduler
        from .views import weekly_mailing
        board_scheduler.add_job(weekly_mailing, 'interval', days=7)
        if os.environ.get('RUN_MAIN'):
            board_scheduler.start()

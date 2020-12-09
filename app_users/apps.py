from django.apps import AppConfig


class AppUsersConfig(AppConfig):
    name = 'app_users'
    verbose_name = '用户'

    # def ready(self):
    #     import app_users.signals

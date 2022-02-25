from django.apps import AppConfig


class MonarchConfig(AppConfig):
    name = "monarch"
    label = "monarch"

    def ready(self):
        # print('ready')
        pass

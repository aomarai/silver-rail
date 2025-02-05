from django.apps import AppConfig


class CharactersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "characters"

    # TODO: Implement stats (frontend might be better for this)
    # def ready(self):
    #     import characters.signals

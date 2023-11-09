from django.apps import AppConfig


class SocialProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_profiles'
    verbose_name = '02.Social Network: Profiles'

    def ready(self):
        import social_profiles.signals

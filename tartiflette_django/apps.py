from importlib import import_module

from django.apps import AppConfig
from django.core.checks import registry

from .checks import check_configuration
from .settings import _setting


class TartifletteAppConfig(AppConfig):
    name = 'tartiflette_django'
    label = "tartiflette"

    def import_graphql(self):
        lookups = _setting("TARTIFLETTE_LOOKUPS")

        if not lookups:
            return

        for app in self.apps.get_app_configs():
            for lookup in lookups:
                lookup_module = "%s.%s" % (app.name, lookup)
                try:
                    import_module(lookup_module)
                except ModuleNotFoundError as e:
                    if e.name != lookup_module and \
                            not lookup_module.startswith(e.name):
                        raise e

    def ready(self):
        self.import_graphql()
        registry.register(check_configuration)


default_app_config = 'tartiflette_django.TartifletteAppConfig'

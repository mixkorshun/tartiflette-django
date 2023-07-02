from django.conf import settings

from .resolvers import create_default_resolver

DEFAULTS = {
    "TARTIFLETTE": None,
    "TARTIFLETTE_SDL": None,

    "TARTIFLETTE_SAFE_DEFAULT_RESOLVER": True,
    "TARTIFLETTE_AUTO_SNAKE_CASE": True,

    "TARTIFLETTE_LOOKUPS": (
        "graphql",
        "graphql.resolvers",
        "graphql.mutations",
        "graphql.subscriptions",
        "graphql.types",
        "graphql.scalars",
        "graphql.directives"
    )
}


def get_engine_config(name):
    root_config = _setting("TARTIFLETTE")

    if root_config is not None:
        try:
            config = root_config[name]
        except KeyError:
            raise KeyError(f"Tartiflette engine '{name}' isn't configured")
    else:
        if name != "default":
            raise KeyError(f"Tartiflette engine '{name}' isn't configured")

        config = {
            "sdl": _setting("TARTIFLETTE_SDL")
        }

    config.setdefault("custom_default_resolver", create_default_resolver(
        safe=_setting("TARTIFLETTE_SAFE_DEFAULT_RESOLVER"),
        to_snake_case=_setting("TARTIFLETTE_AUTO_SNAKE_CASE"),
    ))

    return config


def _setting(name):
    return getattr(settings, name, DEFAULTS.get(name))

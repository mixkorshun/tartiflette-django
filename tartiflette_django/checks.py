import os
from pathlib import Path

from django.conf import settings
from django.core.checks import Error, Warning


def check_configuration(app_configs, **kwargs):
    errors = []

    if hasattr(settings, "TARTIFLETTE"):
        if hasattr(settings, "TARTIFLETTE_SDL"):
            errors.append(Warning(
                "TARTIFLETTE_SDL doesn't make sense when TARTIFLETTE is set",
                hint="Remove TARTIFLETTE_SDL and "
                     "use TARTIFLETTE['default']['sdl'] instead",
                id="tartiflette.W001"
            ))

        for engine_name, engine_config in settings.TARTIFLETTE.items():
            _check_sdl_file(
                sdl=engine_config.get("sdl", None),
                setting_key="TARTIFLETTE['%s']['sdl']" % engine_name
            )
    else:
        sdl = getattr(settings, "TARTIFLETTE_SDL", None)
        errors.extend(_check_sdl_file(sdl, "TARTIFLETTE_SDL"))

    return errors


def _check_sdl_file(sdl, setting_key):
    if not sdl:
        return [
            Error("%s is required" % setting_key,
                  id="tartiflette.E002")
        ]

    if isinstance(sdl, (str, Path)):
        if not os.path.exists(sdl):
            return [
                Error("SDL '%s' isn't exists in filesystem" % sdl,
                      id="tartiflette.E003")
            ]

        return []

    errors = []
    for sdl_file in sdl:
        if not os.path.exists(sdl_file):
            errors.append(
                Error("SDL '%s' isn't exists in filesystem" % sdl,
                      id="tartiflette.E003")
            )
    return errors

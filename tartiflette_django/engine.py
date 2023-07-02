import asyncio

from django.core.exceptions import ImproperlyConfigured
from tartiflette import create_engine as create_tartiflette_engine

from .settings import get_engine_config

_engines = {}


async def get_engine(name="default"):
    if name not in _engines:
        event = asyncio.Event()
        _engines[name] = event

        try:
            _engines[name] = await _create_engine(name)
        except Exception:
            del _engines[name]
            raise
        finally:
            event.set()

    if isinstance(_engines[name], asyncio.Event):
        await _engines[name].wait()

    return _engines[name]


def load_engine(name):
    if name not in _engines:
        _engines[name] = _create_engine(name)


async def _create_engine(name):
    config = get_engine_config(name)
    if not config:
        raise ImproperlyConfigured(
            "Tartiflette schema '%s' isn't configured" % name
        )

    return await create_tartiflette_engine(**config)

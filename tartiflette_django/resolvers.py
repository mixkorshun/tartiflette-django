from asgiref.sync import sync_to_async
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from tartiflette.resolver.default import default_field_resolver

from .utils import camel_to_snake_case


def create_default_resolver(*, safe=False, to_snake_case=True):
    async def django_default_resolver(root, args, ctx, info):
        if to_snake_case:
            field_name = camel_to_snake_case(info.field_name)

        if isinstance(root, models.Model):
            try:
                field = root._meta.get_field(field_name)
            except FieldDoesNotExist:
                if not hasattr(root, field_name):
                    raise RuntimeError(
                        "Can't resolve %(model)s:%(field)s property. "
                        "Most likely because of missed .annotate() call" % {
                            "model": root._meta.label,
                            "field": field_name,
                        }
                    )

                return getattr(root, field_name)

            if field.many_to_one or field.one_to_one:
                if field.concrete:
                    id_value = getattr(root, field.attname)
                    if id_value is None:
                        return None

                if safe and not field.is_cached(root):
                    raise RuntimeError(
                        "Field %(model)s:%(field)s isn't cached. "
                        "Please use .select_related() or dataloader "
                        "to avoid N+1 problem" % {
                            "model": root._meta.label,
                            "field": field_name,
                        }
                    )

                return getattr(root, field_name)

            if field.one_to_many or field.many_to_many:
                _prefetched = getattr(root, "_prefetched_objects_cache", {})

                if safe and field_name not in _prefetched:
                    raise RuntimeError(
                        "Field %(model)s:%(field)s isn't cached. "
                        "Please use .prefetch_related() or dataloader "
                        "to avoid N+1 problem" % {
                            "model": root._meta.label,
                            "field": field_name,
                        }
                    )

                return [obj async for obj in getattr(root, field_name).all()]

            return getattr(root, field_name)

        return await default_field_resolver(root, args, ctx, info)

    return django_default_resolver


@sync_to_async
def _get_foreign_object(root, field):
    return getattr(root, field)

import graphene
import redis
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import CoreAPICompatInspector, NotHandled, FieldInspector, SwaggerAutoSchema

from info_graphql.settings import CACHEOPS_REDIS


def str_to_enum(name):
    return name.replace(" ", "_").replace("-", "_").upper()


def to_enum(enum_cls, *, type_name=None, **options) -> graphene.Enum:
    deprecation_reason = getattr(enum_cls, "__deprecation_reason__", None)
    if deprecation_reason:
        options.setdefault("deprecation_reason", deprecation_reason)

    type_name = type_name or (enum_cls.__name__ + "Enum")
    enum_data = [(str_to_enum(code.upper()), code) for code, name in enum_cls.CHOICES]
    return graphene.Enum(type_name, enum_data, **options)


class DjangoFilterDescriptionInspector(CoreAPICompatInspector):
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, DjangoFilterBackend):
            result = super(DjangoFilterDescriptionInspector, self).get_filter_parameters(filter_backend)
            for param in result:
                if not param.get('description', ''):
                    param.description = "Filter the returned list by {field_name}".format(field_name=param.name)

            return result

        return NotHandled


class NoSchemaTitleInspector(FieldInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        if isinstance(result, openapi.Schema.OR_REF):
            schema = openapi.resolve_ref(result, self.components)
            schema.pop('title', None)

        return result


class NoTitleAutoSchema(SwaggerAutoSchema):
    field_inspectors = [NoSchemaTitleInspector] + swagger_settings.DEFAULT_FIELD_INSPECTORS


class NoPagingAutoSchema(NoTitleAutoSchema):
    def should_page(self):
        return False


class ConnectionValidations:
    @staticmethod
    def redis_connection_validation():
        try:
            conn = redis.StrictRedis(
                host=CACHEOPS_REDIS.host,
                port=CACHEOPS_REDIS.port)
            conn.ping()
            return True
        except:
            return False

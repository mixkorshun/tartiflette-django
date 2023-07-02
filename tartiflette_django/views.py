import asyncio.coroutines
import json

from django.conf import settings
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import classonlymethod, method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .engine import get_engine


@method_decorator(csrf_exempt, name="dispatch")
class GraphQLView(View):
    engine_name = "default"

    graphiql_enabled = None
    graphiql_template_name = "tartiflette/graphiql.html"
    graphiql_settings = None

    def get_graphiql_enabled(self):
        if self.graphiql_enabled is None:
            return settings.DEBUG

        return self.graphiql_enabled

    def get_graphiql_template_name(self):
        return self.graphiql_template_name

    def get_graphiql_settings(self):
        return self.graphiql_settings or {}

    def get_engine_name(self):
        return self.engine_name

    def get_graphql_root_value(self):
        return {}

    def get_graphql_context(self):
        return {
            "request": self.request
        }

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def get(self, request, *args, **kwargs):
        if not self.get_graphiql_enabled():
            return HttpResponseBadRequest()

        return render(request, self.get_graphiql_template_name(), context={
            "path": request.path,
            "settings": json.dumps(self.get_graphiql_settings()),
        })

    async def post(self, request, *args, **kwargs):
        engine = await get_engine(self.get_engine_name())

        try:
            data = self.parse_request(request)
        except ValueError as e:
            return HttpResponseBadRequest(*e.args)

        query = data["query"]
        operation_name = data.get("operationName")
        variables = data.get("variables")

        execution_result = await self.execute_graphql(
            engine,
            query,
            operation_name=operation_name,
            variables=variables
        )

        return self.create_response(execution_result)

    def parse_request(self, request: HttpRequest):
        if request.content_type == "application/graphql":
            try:
                data = {
                    "query": request.body.decode()
                }
            except Exception:
                raise ValueError("Invalid request body")

        elif request.content_type in [
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ]:
            data = request.POST.copy()

        elif request.content_type == "application/json":
            try:
                data = json.loads(request.body.decode("utf-8"))
            except Exception:
                raise ValueError("Invalid request body")
        else:
            raise ValueError("Unsupported content type")

        data["operationName"] = (
                data.get("operationName")
                or request.GET.get("operationName")
        )

        return data

    async def execute_graphql(self, engine, query, *, operation_name=None,
                              variables=None):
        return await engine.execute(
            query=query,
            operation_name=operation_name,
            variables=variables,
            context=self.get_graphql_context(),
            initial_value=self.get_graphql_root_value(),
        )

    def create_response(self, execution_result):
        data = execution_result.get("data")
        errors = execution_result.get("errors")

        status_code = 200
        if data is None and errors:
            status_code = 400

        return HttpResponse(json.dumps({
            "data": data,
            "errors": errors,
        }), status=status_code, content_type="application/json")

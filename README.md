![Tartiflette Django](https://github.com/mixkorshun/tartiflette-django/blob/main/github-landing.png)

**tartiflette-django** is an integration of Tartiflette GraphQL Engine to `Django` framework. You can take a look at the [Tartiflette API documentation](https://tartiflette.io/docs/welcome/what-is-tartiflette).

## Installation
`tartiflette-django` is available on [pypi.org](https://pypi.org/project/tartiflette-django/).

**WARNING**: Do not forget to install the [tartiflette dependencies beforehand as explained in the tutorial](https://tartiflette.io/docs/tutorial/install-tartiflette/).

```bash
pip install tartiflette-django
```

## Requirements
`tartiflette-django` is compatible with:

- Python 3.6+.
- Django 3.0+.
- Tartiflette 1.x.

## Quickstart

First, add GraphQL schema to your application:
```graphql
# `<django_proj>/schema.graphql`

type User {
  id: ID!
  firstName: String!
  lastName: String!
  email: String!
}

type Query {
  currentUser: User
}

schema { query: Query }
```

Configure Tartiflette by setting path to your GraphQL schema in Django settings.

```python
# `<django_proj>/settings.py`

# ...
TARTIFLETTE_SDL = BASE_DIR / "<django_proj>" / "schema.graphql"
# ...
```

Create url for GraphQL endpoint:
```python
# `<django_proj>/urls.py`

from django.urls import path
from tartiflette_django.views import GraphQLView

urlpatterns = [
    path('graphql/', GraphQLView.as_view()),
    # ...
]
```

And write your resolvers in `<django_app>/graphql.py` or `<django_app>/graphql/resolvers.py`:
```python
# <django_app>/graphql/resolvers.py

from tartiflette import Resolver

@Resolver("Query.currentUser")
async def resolve_current_user(parent, args, context, info):
    user = context["request"].user
    if not user.is_authenticated:
        return None

    return user
```

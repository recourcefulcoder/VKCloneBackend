from fastapi import Depends

import strawberry
from strawberry.fastapi import BaseContext, GraphQLRouter


class CustomContext(BaseContext):
    def __init__(self, greeting: str, name: str):
        self.greeting = greeting
        self.name = name


def custom_context_dependency() -> CustomContext:
    return CustomContext(greeting="you rock!", name="John")


async def get_context(
    custom_context=Depends(custom_context_dependency),
):
    return custom_context


@strawberry.type
class Post:
    id: int
    author_id: int

    title: str
    content: str

    created_date: int
    last_edit: int


schema = strawberry.Schema(Post)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

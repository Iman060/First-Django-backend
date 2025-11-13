"""
GraphQL schema for PredictHub
"""
import strawberry
from strawberry.django import auth
from typing import List, Optional
from datetime import datetime

# Placeholder for GraphQL schema - will be expanded with actual types
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from PredictHub GraphQL API"

schema = strawberry.Schema(query=Query)


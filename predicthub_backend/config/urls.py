"""
URL configuration for predicthub_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from strawberry.django.views import GraphQLView
from .graphql_schema import schema

schema_view = get_schema_view(
    openapi.Info(
        title="PredictHub API",
        default_version='v1',
        description="Community Prediction Market Backend API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@predicthub.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # GraphQL
    path('graphql/', GraphQLView.as_view(schema=schema)),
    
    # API Routes
    path('auth/', include('users.urls')),
    path('markets/', include('markets.urls')),
    path('trades/', include('trades.urls')),
    path('users/', include('users.urls')),
    path('leaderboard/', include('analytics.urls')),
    path('webhook/', include('indexer.urls')),
]


"""
URL configuration for predicthub_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from strawberry.django.views import GraphQLView
from .graphql_schema import schema
from indexer.views import OnchainWebhookView
from webhooks.onchain_webhook import onchain_webhook


def api_root(request):
    """Root API endpoint with API information"""
    return JsonResponse({
        'name': 'PredictHub API',
        'version': '1.0.0',
        'description': 'Community Prediction Market Backend API',
        'endpoints': {
            'authentication': '/auth/',
            'markets': '/markets/',
            'trades': '/trades/',
            'leaderboard': '/leaderboard/',
            'admin': '/admin/',
            'api_docs': '/swagger/',
            'graphql': '/graphql/',
        },
        'documentation': {
            'swagger': '/swagger/',
            'redoc': '/redoc/',
        }
    })

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
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # GraphQL
    path('graphql/', GraphQLView.as_view(schema=schema)),
    path('api/webhook/onchain/', OnchainWebhookView.as_view(), name='onchain-webhook'),
    path('webhooks/onchain/', onchain_webhook, name='onchain-webhook-new'),
    
    # API Routes
    path('auth/', include('users.urls')),  # Auth endpoints (signup, login, me)
    path('markets/', include('markets.urls')),
    path('trades/', include('trades.urls')),
    path('leaderboard/', include('analytics.urls')),
    path('webhook/', include('indexer.urls')),
]


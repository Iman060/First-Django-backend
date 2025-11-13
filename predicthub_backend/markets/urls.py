from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarketViewSet, MarketCreateViewSet
from trades.views import create_trade

router = DefaultRouter()
router.register(r'', MarketViewSet, basename='market')
router.register(r'create', MarketCreateViewSet, basename='market-create')

app_name = 'markets'

urlpatterns = [
    path('', include(router.urls)),
    path('<int:market_id>/trade/', create_trade, name='market_trade'),
]


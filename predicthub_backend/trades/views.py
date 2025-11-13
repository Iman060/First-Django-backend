from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal
from .models import Trade
from .serializers import TradeSerializer, TradeCreateSerializer
from markets.models import Market, OutcomeToken, PriceHistory
from positions.models import Position


class TradeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing trades"""
    queryset = Trade.objects.select_related('user', 'market').all()
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        market_id = self.request.query_params.get('market', None)
        
        if market_id:
            queryset = queryset.filter(market_id=market_id)
        
        return queryset


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_trade(request, market_id):
    """Create a trade for a specific market"""
    serializer = TradeCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        market = Market.objects.get(id=market_id)
    except Market.DoesNotExist:
        return Response(
            {'error': 'Market not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if market.status != 'active':
        return Response(
            {'error': 'Market is not active'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    outcome_type = serializer.validated_data['outcome_type']
    trade_type = serializer.validated_data['trade_type']
    amount_staked = Decimal(str(serializer.validated_data['amount_staked']))
    
    with transaction.atomic():
        # Get or create outcome tokens
        yes_token, _ = OutcomeToken.objects.get_or_create(
            market=market,
            outcome_type='YES',
            defaults={'supply': 0, 'price': 0.5}
        )
        no_token, _ = OutcomeToken.objects.get_or_create(
            market=market,
            outcome_type='NO',
            defaults={'supply': 0, 'price': 0.5}
        )
        
        # Calculate current prices using AMM
        total_liquidity = yes_token.supply + no_token.supply
        if total_liquidity == 0:
            # Initialize with equal liquidity
            yes_token.supply = amount_staked / 2
            no_token.supply = amount_staked / 2
            yes_price = Decimal('0.5')
            no_price = Decimal('0.5')
        else:
            yes_price = yes_token.supply / total_liquidity
            no_price = no_token.supply / total_liquidity
        
        # Execute trade
        target_token = yes_token if outcome_type == 'YES' else no_token
        price_at_execution = yes_price if outcome_type == 'YES' else no_price
        
        if trade_type == 'buy':
            # Calculate tokens to receive
            tokens_amount = amount_staked / price_at_execution if price_at_execution > 0 else amount_staked * 2
            target_token.supply += amount_staked
        else:  # sell
            # User must have enough tokens
            position, _ = Position.objects.get_or_create(
                user=request.user,
                market=market,
                defaults={'yes_tokens': 0, 'no_tokens': 0, 'total_staked': 0}
            )
            
            user_tokens = position.yes_tokens if outcome_type == 'YES' else position.no_tokens
            if user_tokens < amount_staked:
                return Response(
                    {'error': 'Insufficient tokens'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            tokens_amount = amount_staked * price_at_execution
            target_token.supply -= amount_staked
        
        target_token.price = target_token.supply / (yes_token.supply + no_token.supply) if (yes_token.supply + no_token.supply) > 0 else Decimal('0.5')
        target_token.save()
        
        # Update other token price
        other_token = no_token if outcome_type == 'YES' else yes_token
        other_token.price = other_token.supply / (yes_token.supply + no_token.supply) if (yes_token.supply + no_token.supply) > 0 else Decimal('0.5')
        other_token.save()
        
        # Update market liquidity
        market.liquidity_pool = yes_token.supply + no_token.supply
        market.save()
        
        # Create trade record
        trade = Trade.objects.create(
            user=request.user,
            market=market,
            outcome_type=outcome_type,
            trade_type=trade_type,
            amount_staked=amount_staked,
            tokens_amount=tokens_amount,
            price_at_execution=price_at_execution
        )
        
        # Update position
        position, _ = Position.objects.get_or_create(
            user=request.user,
            market=market,
            defaults={'yes_tokens': 0, 'no_tokens': 0, 'total_staked': 0}
        )
        
        if trade_type == 'buy':
            if outcome_type == 'YES':
                position.yes_tokens += tokens_amount
            else:
                position.no_tokens += tokens_amount
            position.total_staked += amount_staked
        else:  # sell
            if outcome_type == 'YES':
                position.yes_tokens -= amount_staked
            else:
                position.no_tokens -= amount_staked
            position.total_staked -= amount_staked
        
        position.save()
        
        # Record price history
        PriceHistory.objects.create(
            market=market,
            yes_price=yes_token.price,
            no_price=no_token.price
        )
    
    serializer = TradeSerializer(trade)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_trades(request):
    """Get current user's trades"""
    trades = Trade.objects.filter(user=request.user).order_by('-created_at')
    
    from rest_framework.pagination import PageNumberPagination
    paginator = PageNumberPagination()
    page = paginator.paginate_queryset(trades, request)
    serializer = TradeSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


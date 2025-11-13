from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from users.models import User
from users.serializers import UserSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def global_leaderboard(request):
    """Get global leaderboard"""
    users = User.objects.all().order_by('-total_points')[:100]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def weekly_leaderboard(request):
    """Get weekly leaderboard"""
    week_ago = timezone.now() - timedelta(days=7)
    # This would need to be calculated based on points earned in the last week
    # For now, returning top users
    users = User.objects.all().order_by('-total_points')[:100]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def monthly_leaderboard(request):
    """Get monthly leaderboard"""
    month_ago = timezone.now() - timedelta(days=30)
    # This would need to be calculated based on points earned in the last month
    # For now, returning top users
    users = User.objects.all().order_by('-total_points')[:100]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_leaderboard(request, user_id):
    """Get specific user's leaderboard position"""
    try:
        user = User.objects.get(id=user_id)
        # Calculate rank
        rank = User.objects.filter(total_points__gt=user.total_points).count() + 1
        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data,
            'rank': rank
        })
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


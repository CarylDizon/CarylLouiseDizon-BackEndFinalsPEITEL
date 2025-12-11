from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Simple user registration endpoint
    Accepts: username, password, password2, email (optional)
    Returns: token and user info
    """
    try:
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()
        password2 = request.data.get('password2', '').strip()
        email = request.data.get('email', '').strip() or None
        
        # Validation
        if not username or not password or not password2:
            return Response(
                {'error': 'Username and passwords are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if password != password2:
            return Response(
                {'password2': ['Passwords do not match']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(password) < 3:
            return Response(
                {'password': ['Password must be at least 3 characters']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email or ''
            )
        except IntegrityError:
            return Response(
                {'username': ['Username already exists']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'key': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

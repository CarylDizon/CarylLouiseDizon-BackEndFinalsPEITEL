# media_tracker/serializers.py

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import MediaItem

# --- Custom Registration Serializer ---
class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom serializer that accepts 'password' and 'password2' fields
    instead of Django's default 'password1' and 'password2'
    """
    
    email = serializers.EmailField(required=False, allow_blank=True)
    
    # Accept 'password' from frontend
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        # Call parent validation
        data['password1'] = data.pop('password')  # Rename for parent validator
        super().validate(data)
        
        # Check passwords match
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError({"password2": "Passwords do not match."})
            
        return data
    
    def save(self, request=None):
        user = super().save(request)
        # Ensure token is created
        Token.objects.get_or_create(user=user)
        return user

# --- Existing Media Item Serializer ---
class MediaItemSerializer(serializers.ModelSerializer):
    # The 'owner' field is read-only. It displays the owner's username (which is the user who created it).
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = MediaItem
        # Ensure 'time_hours' is included for the frontend's burden calculation
        fields = ('id', 'owner', 'owner_username', 'title', 'media_type', 'status', 'time_hours', 'is_favorite', 'deleted', 'created_at', 'updated_at')
        read_only_fields = ('owner', 'created_at', 'updated_at')
"""
User Serializers
These serializers handle conversion between User model and JSON data.
"""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Why Serializer and not ModelSerializer?
    - We're not directly working with a model here
    - We're validating login credentials (username + password)
    - This is a "data-only" serializer for validation
    """
    
    # Define the fields we expect from frontend
    username = serializers.CharField(
        required=True,
        help_text="Username for login"
    )
    password = serializers.CharField(
        required=True,
        write_only=True,  # Never send password back in response
        style={'input_type': 'password'},  # UI hint for password field
        help_text="User password"
    )
    
    def validate(self, data):
        """
        Custom validation method.
        
        This runs after individual field validation.
        Here we check if username/password combination is correct.
        
        Args:
            data (dict): Dictionary containing username and password
            
        Returns:
            dict: Validated data with user object
            
        Raises:
            ValidationError: If credentials are invalid
        """
        username = data.get('username')
        password = data.get('password')
        
        # authenticate() is Django's built-in function
        # It checks if username/password match a user in database
        # Returns User object if valid, None if invalid
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Credentials are invalid
            raise serializers.ValidationError(
                "Invalid username or password.",
                code='authentication'
            )
        
        if not user.is_active:
            # User exists but account is deactivated
            raise serializers.ValidationError(
                "User account is disabled.",
                code='authentication'
            )
        
        # Add user object to validated data
        # We'll use this in the view to generate token
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    
    Why ModelSerializer?
    - We're working directly with the User model
    - ModelSerializer automatically creates fields based on model
    - Reduces code duplication
    
    This is used to return user information after login or in profile.
    """
    
    class Meta:
        model = User  # Which model to serialize
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        # We deliberately exclude 'password' for security
        # Never send password (even hashed) in API responses
        
        # Make fields read-only (can't be changed via this serializer)
        read_only_fields = ['id']


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer for login response.
    
    This defines the structure of data we send back after successful login.
    It's used for API documentation and validation.
    """
    
    token = serializers.CharField(
        help_text="Authentication token to use in subsequent requests"
    )
    user = UserSerializer(
        help_text="User information"
    )
    
    # Note: This is a response-only serializer
    # We never receive data in this format, only send it
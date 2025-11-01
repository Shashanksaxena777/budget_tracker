"""
User Views (API Endpoints)
These views handle authentication-related API requests.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import LoginSerializer, UserSerializer, LoginResponseSerializer


@api_view(['POST'])
@permission_classes([AllowAny])  # Anyone can access login (not just authenticated users)
def login_view(request):
    """
    User Login API Endpoint
    
    What is @api_view?
    - Decorator that converts a function into a DRF API view
    - Handles request parsing, response formatting
    - Adds browsable API interface
    
    What is @permission_classes([AllowAny])?
    - By default, all APIs require authentication (from settings.py)
    - This decorator overrides that default
    - Allows anyone to access this endpoint (because you can't login if you're not authenticated!)
    
    Method: POST
    URL: /api/auth/login/
    
    Request Body:
    {
        "username": "testuser",
        "password": "testpass123"
    }
    
    Success Response (200):
    {
        "token": "a1b2c3d4e5f6...",
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
    }
    
    Error Response (400):
    {
        "error": "Invalid username or password."
    }
    """
    
    # Step 1: Create serializer with incoming data
    # request.data contains the JSON data sent by frontend
    serializer = LoginSerializer(data=request.data)
    
    # Step 2: Validate the data
    # is_valid() calls the validate() method we defined
    # raise_exception=True automatically returns 400 error if validation fails
    if not serializer.is_valid():
        # Return validation errors
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Step 3: Get the validated user
    # After is_valid(), validated_data contains cleaned data
    # We added 'user' in the validate() method
    user = serializer.validated_data['user']
    
    # Step 4: Get or create authentication token
    # Token.objects.get_or_create() is like:
    # - Check if user has a token → return it
    # - If not → create new token → return it
    # Returns: (token_object, created_boolean)
    token, created = Token.objects.get_or_create(user=user)
    
    # Step 5: Serialize user data
    # Convert User object to JSON format
    user_serializer = UserSerializer(user)
    
    # Step 6: Prepare response data
    response_data = {
        'token': token.key,  # token.key is the actual token string
        'user': user_serializer.data  # User information as JSON
    }
    
    # Step 7: Return response
    return Response(
        response_data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def logout_view(request):
    """
    User Logout API Endpoint
    
    This endpoint requires authentication (notice no @permission_classes([AllowAny]))
    
    Method: POST
    URL: /api/auth/logout/
    Headers: Authorization: Token <user_token>
    
    Success Response (200):
    {
        "message": "Successfully logged out."
    }
    
    How token authentication works:
    1. Frontend stores token after login
    2. For each API request, frontend sends: 
       Header: "Authorization: Token abc123xyz"
    3. DRF's TokenAuthentication checks if token exists
    4. If valid, sets request.user to the User object
    5. If invalid, returns 401 Unauthorized
    """
    
    # request.user is set by TokenAuthentication middleware
    # It contains the User object of the authenticated user
    
    try:
        # Delete the user's token
        # This effectively logs them out
        # After deletion, the old token becomes invalid
        request.user.auth_token.delete()
        
        return Response(
            {'message': 'Successfully logged out.'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': 'Something went wrong during logout.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def user_profile(request):
    """
    Get Current User Profile
    
    Method: GET
    URL: /api/auth/profile/
    Headers: Authorization: Token <user_token>
    
    Success Response (200):
    {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
    }
    
    This endpoint is useful to:
    - Verify token is still valid
    - Get current user information
    - Check if user is logged in
    """
    
    # Serialize current user
    serializer = UserSerializer(request.user)
    
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
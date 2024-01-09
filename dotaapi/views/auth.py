from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import date
from rest_framework import serializers, status

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of an employee

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'token': token.key
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new employee for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    if User.objects.filter(email=request.data['email']):
        return Response('Duplicate Email Found')

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['firstName'],
        last_name=request.data['lastName'],
        email=request.data['email']
        )

    # Now save the extra info in the employee table
    # employee = Employee.objects.create(
    #     user=new_user,
    #     hourly_rate=request.data['hourlyRate'],
    #     hire_date=date.today()
    # )

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)
    # Return the token to the client
    data = { 'token': token.key }
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])
def getMe(request):

    if request.auth:
        user = User.objects.get(username=request.auth.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        data = 'Not found'
        return Response(data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = User
        fields = ('id', 'username')


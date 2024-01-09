"""View module for handling requests about employees"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dotaapi.models import Profile
from datetime import date


class ProfileView(ViewSet):
    """randomzer profile view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single profile

        Returns:
            Response -- JSON serialized employee
        """

        profile = Profile.objects.get(pk=pk)


        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all profiles for a user

        Returns:
            Response -- JSON serialized list of employees
        """

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True) 
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized profile instance
        """

        user = User.objects.get(pk=request.data['user'])

        profile = Profile.objects.create(
            user=user,
            name=request.data['name'],
            )

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a profile

        Returns:
            Response -- Empty body with 204 status code
        """

        profile = Profile.objects.get(pk=request.data['id'])
        user = User.objects.get(pk=request.data['user_id'])
        
        profile.name = request.data['name']

        profile.save()
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

        



class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for profiles
    """
    class Meta:
        model = Profile
        fields = ('id', 'user', 'banned')
        depth = 1
"""View module for handling requests about employees"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dotaapi.models import Profile, BannedHeroes, Hero
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
        me = User.objects.get(id=request.auth.user.id)


        if 'mine' in request.query_params:
            profiles = profiles.filter(user=me)

        serializer = ProfileSerializer(profiles, many=True) 
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized profile instance
        """

        user = User.objects.get(id=request.auth.user.id)

        newProfile = Profile.objects.create(
            user=user,
            name=request.data['title']
            )

        chosenHeroes = request.data
        count = 1
        while count < 125:
            countStr = str(count)
            if chosenHeroes[countStr]:
                count += 1
                continue
            else:
                test = 'stuff'
                bannedHero = BannedHeroes.objects.create(
                    hero = Hero.objects.get(id=count),
                    profile = Profile.objects.get(id=newProfile.id)
                )
                count +=1
            

        serializer = ProfileSerializer(newProfile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a profile

        Returns:
            Response -- Empty body with 204 status code
        """

        profile = Profile.objects.get(pk=pk)
        
        profile.name = request.data['title']

        chosenHeroes = request.data
        count = 1
        while count < 125:
            countStr = str(count)
            currentHeroBan = Hero.objects.get(pk=count)
            try:
                banObject = BannedHeroes.objects.get(
                    hero = currentHeroBan,
                    profile = profile
                )
            except:
                banObject = False

            if chosenHeroes[countStr]:
                count += 1
                if banObject:
                    banObject.delete()
            else:
                if banObject:
                    count +=1
                    continue
                else:
                    BannedHeroes.objects.create(
                        hero = currentHeroBan,
                        profile = profile
                    )
                    count +=1

        profile.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request):
        """Handle Delete requests for a profile. 
        
        Returns """


        profile = Profile.objects.get(pk=request.data)
        user = User.objects.get(id=request.auth.user.id)

        if profile.user == user:
            profile.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)




class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for profiles
    """
    class Meta:
        model = Profile
        fields = ('id', 'user', 'name', 'banned')
        depth = 1
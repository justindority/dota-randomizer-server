"""View module for handling requests about employees"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dotaapi.models import Profile, Hero
from datetime import date
import random


class HeroView(ViewSet):
    """hero view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single hero

        Returns:
            Response -- JSON serialized hero
        """

        hero = Hero.objects.get(pk=pk)


        serializer = HeroSerializer(hero)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all heroes

        Returns:
            Response -- JSON serialized list of heroes
        """

        heroes = list(Hero.objects.all())

        serializer = HeroSerializer(heroes, many=True) 
        return Response(serializer.data)



        



class HeroSerializer(serializers.ModelSerializer):
    """JSON serializer for profiles
    """
    class Meta:
        model = Hero
        fields = ('id', 'name', 'attribute', 'portraiturl', 'iconurl')
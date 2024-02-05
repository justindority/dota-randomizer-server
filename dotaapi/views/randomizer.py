"""View module for handling requests about employees"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dotaapi.models import Profile, Hero
from datetime import date
import random


class RandomizerView(ViewSet):
    """randomizer view"""

    def retrieve(self, request, pk):
        """Handle GET requests for custom randoming a hero. needs to have
        a selected custom random set.

        Returns:
            Response -- JSON serialized hero
        """

        heroes = Hero.objects.all()

        profile = Profile.objects.get(pk=pk)
        heroesFilter = heroes.exclude(id__in=profile.banned.all())
        hero = random.choice(heroesFilter)

        serializer = HeroSerializer(hero)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests for custom randoming a hero. needs to have
        a selected custom random set.

        Returns:
            Response -- JSON serialized hero
        """

        heroes = Hero.objects.all()

        if 'true' in request.query_params:
            hero = random.choice(heroes)

        if 'str' in request.query_params:
            strHeroes = heroes.filter(attribute = 'str')
            hero = random.choice(strHeroes)

        if 'agi' in request.query_params:
            agiHeroes = heroes.filter(attribute = 'agi')
            hero = random.choice(agiHeroes)

        if 'int' in request.query_params:
            intHeroes = heroes.filter(attribute = 'int')
            hero = random.choice(intHeroes)

        if 'uni' in request.query_params:
            uniHeroes = heroes.filter(attribute = 'uni')
            hero = random.choice(uniHeroes)
        

        if hero:
            serializer = HeroSerializer(hero)
            return Response(serializer.data)




class HeroSerializer(serializers.ModelSerializer):
    """JSON serializer for profiles
    """
    class Meta:
        model = Hero
        fields = ('id', 'name', 'attribute', 'portraiturl', 'iconurl')
import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.types import ObjectType

from django_graphql_movies.movies.models import Actor
from django_graphql_movies.movies.models import Movie


class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class Query(ObjectType):
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)

    def resolve_actor(self, info, **kwargs):
        actor_id = kwargs.get('id')

        if not actor_id:
            return Actor.objects.get(pk=actor_id)

        return None

    def resolve_movie(self, info, **kwargs):
        movie_id = kwargs.get('id')

        if not movie_id:
            return Movie.objects.get(pk=movie_id)

        return None

    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()

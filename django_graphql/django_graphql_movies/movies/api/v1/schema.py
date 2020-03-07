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
            return None

        return Actor.objects.get(pk=actor_id)

    def resolve_movie(self, info, **kwargs):
        movie_id = kwargs.get('id')

        if not movie_id:
            return None

        return Movie.objects.get(pk=movie_id)

    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()


class ActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class MovieInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()


class CreateActor(graphene.Mutation):
    class Arguments:
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input=None):
        actor_instance = Actor(name=input.name)
        actor_instance.save()

        return CreateActor(ok=True, actor=actor_instance)


class UpdateActor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        actor_instance = Actor.objects.get(pk=id)

        if actor_instance:
            actor_instance.name = input.name
            actor_instance.save()

            return UpdateActor(ok=True, actor=actor_instance)

        return UpdateActor(ok=False, actor=None)


class CreateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, input=None):
        actors = []

        for actor_input in input.actors:
            actor = Actor.objects.get(pk=actor_input.id)

            if not actor:
                return CreateMovie(ok=False, movie=None)

            actors.append(actor)

        movie_instance = Movie(title=input.title, year=input.year)
        movie_instance.save()
        movie_instance.actors.set(actors)

        return CreateMovie(ok=True, movie=movie_instance)


class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input=None):
        movie_instance = Movie.objects.get(pk=id)

        if not movie_instance:
            return UpdateMovie(ok=False, movie=None)

        actors = []
        for actor_input in input.actors:
            actor = Actor.objects.get(pk=actor_input.id)

            if not actor:
                return UpdateMovie(ok=False, movie=None)

            actors.append(actor)

        movie_instance.title = input.title
        movie_instance.year = input.year
        movie_instance.save()
        movie_instance.actors.set(actors)

        return UpdateMovie(ok=True, movie=movie_instance)


class Mutation(ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


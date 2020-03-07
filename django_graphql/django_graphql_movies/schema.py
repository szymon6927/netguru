import graphene

from django_graphql_movies.movies.api.v1.schema import Query as MovieAppQuery
from django_graphql_movies.movies.api.v1.schema import Mutation as MovieAppMutation


class Query(MovieAppQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(MovieAppMutation, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

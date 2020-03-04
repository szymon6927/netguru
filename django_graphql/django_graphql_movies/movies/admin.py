from django.contrib import admin

from django_graphql_movies.movies.models import Actor
from django_graphql_movies.movies.models import Movie

admin.site.register(Actor)
admin.site.register(Movie)

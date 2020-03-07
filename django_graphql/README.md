### django_graphql_movies

Netguru GraphQL training

URL: `http://127.0.0.1:8000/graphql/`


### Desc



- get all movies

```
query getMovies {
  movies {
    id
    title
    actors {
      id
      name
    }
  }
}
```
- get all actors

```
query getActors {
  actors {
    id
    name
  }
}
```

- get single movie

```
query getMovie {
  movie(id: <movie_id>) {
    id
    title
    actors {
      id
      name
    }
  }
}
```

- add actor

```
mutation createActor {
  createActor(input: {
    name: "Szymon Miks"
  }) {
    ok
    actor {
      id
      name
    }
  }
}
```

- add movie

```
mutation createMovie {
  createMovie(input: {
    title: "Miodowe lata",
    actors: [
      {
        id: <actor_id>
      }
    ]
    year: 1999
  }) {
    ok
    movie{
      id
      title
      actors {
        id
        name
      }
      year
    }
  }
}
```

- update movie

```
mutation updateMovie {
  updateMovie(id: <movie_id>, input: {
    title: "Miodowe lata - sezon 2",
    actors: [
      {
        id: 3
      }
    ]
    year: 2000
  }) {
    ok
    movie{
      id
      title
      actors {
        id
        name
      }
      year
    }
  }
}
```

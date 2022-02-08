# Free Tomorrow (Backend API)

![free-tomorrow](https://circleci.com/gh/free-tomorrow/free_tomorrow_backend.svg?style=svg)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)

#### BE Team: [Sam Devine](https://github.com/samueldevine), [Greg Fischer](https://github.com/GregoryJFischer) || FE Team: [Delilah Necrason](https://github.com/delilahrois), [Regan Losey](https://github.com/reganlosey)

-------------------------------------------------------------------------------

**WIP**

Free Tomorrow is an app designed to help busy friends schedule a trip together. The backend repository is responsible for storing information about each user and their availability in a PostgreSQL database, exposing any required information about users or trips to the frontend, and performing the required logic to determine available dates for each invited user. Authentication is not currently supported, and users must simply provide a valid email address to create an account, or use an existing email address to log in.

### Endpoints

The base path to access the API is:

```
https://free-tomorrow-be.herokuapp.com/{query}
```

where **{query}** should be replaced with one of the following endpoints.

#### Get All Users

`GET /users/`

Returns a collection of all valid users currently saved in the database, as well as an array of trips associated with each user.

Example response:
```
[
    {
        "id": 1,
        "name": "Bob",
        "email": "bob@example.com",
        "trip_set": []
    },
    {
        "id": 2,
        "name": "Boris",
        "email": "boris@example.com",
        "trip_set": []
    },
    ...
]
```

#### Get A Single User

`GET /users/{id}`

Returns a single user that matches the provided id. If there are no users that match the given id, a 404 status code and error message will be returned.

Example response:
```
{
    "id": 1,
    "name": "Bob",
    "email": "bob@example.com",
    "trip_set": []
}
```

#### Create A New User

```
POST /users/
Content-Type: application/json
Accept: application/json

{
  "name": "Bob"
  "email": "bob@example.com"
}
```

Returns a 201 status code and the id and information of a successfully created user. If there is an issue with creating the user, a 400 status code will be returned with a description of the issue.

Example response:
```
{
    "id": 1,
    "name": "Bob",
    "email": "bob@example.com"
}
```

#### Get All Trips

`GET /trips/`

Returns an array of all valid trips currently saved in the database, as well as an array of users associated with each trip.

Example response:
```
[
    {
        "id": 1,
        "name": "Disney",
        "created_by": "Bob",
        "budget": 1500,
        "confirmed": true,
        "users": []
    },
    {
        "id": 2,
        "name": "Japan",
        "created_by": "George",
        "budget": 2000,
        "confirmed": true,
        "users": []
    },
    ...
]
```

#### Get A Single Trip

`GET /trips/{id}`

Returns a single trip that matches the provided id. If there are no trips that match the given id, a 404 status code and error message will be returned.

Example response:
```
{
    "id": 1,
    "name": "Disney",
    "created_by": "Bob",
    "budget": 1500,
    "confirmed": true,
    "users": []
}
```

#### Create A New trip

```
POST /trips/
Content-Type: application/json
Accept: application/json

{
    "name": "Disney",
    "created_by": "Bob",
    "budget": 2000,
    "confirmed": true
}
```

Returns a 201 status code and the id and information of a successfully created trip. If there is an issue with creating the trip, a 400 status code will be returned instead, along with a description of the issue.

Example response:
```
{
    "id": 1,
    "name": "Disney",
    "created_by": "Bob",
    "budget": 2000,
    "confirmed": true,
    "users": []
}
```

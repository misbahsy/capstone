# Magic Shows Agency

Site live at : [https://magic-cap.herokuapp.com/](https://magic-cap.herokuapp.com)


The project in this repo builds the backend of a magic show agency who manages and assigns magicians to shows. It is part of the Udacity's fullstack nanodegree program.

## API

In order to use the API users need to be authenticated. Jwt tokens can be generated by logging in with the provided credentials on the hosted site.

### Endpoints

#### GET /shows

- General:

  - Returns all the shows.
  - Roles authorized : Assistant, Director, Producer.

- Sample: `curl http://127.0.0.1:5000/shows`

```json
{
  "shows": [
    {
      "id": 1,
      "show_date": "Mon, 06 May 2019 00:00:00 GMT",
      "show_name": "Prisoner of Azkaban"
    },
    {
      "id": 2,
      "show_date": "Tue, 06 May 2003 00:00:00 GMT",
      "show_name": "Magic Wand"
    }
  ],
  "success": true
}
```

#### GET /shows/\<int:id\>

- General:

  - Route for getting a specific show.
  - Roles authorized :  Assistant, Director, Producer.

- Sample: `curl http://127.0.0.1:5000/shows/1`

```json
{
  "show": {
    "id": 1,
    "show_date": "Mon, 06 May 2019 00:00:00 GMT",
    "show_name": "Magic Wand"
  },
  "success": true
}
```

#### POST /shows

- General:

  - Creates a new show based on a payload.
  - Roles authorized : Producer.

- Sample: `curl http://127.0.0.1:5000/shows -X POST -H "Content-Type: application/json" -d '{ "show_name": "Harry Potter", "show_date": "2020-05-06" }'`

```json
{
  "show": {
    "id": 3,
    "show_date": "Wed, 06 May 2020 00:00:00 GMT",
    "show_name": "Harry Potter"
  },
  "success": true
}
```

#### PATCH /shows/\<int:id\>

- General:

  - Patches a show based on a payload.
  - Roles authorized : Director, Producer.

- Sample: `curl http://127.0.0.1:5000/shows/3 -X POST -H "Content-Type: application/json" -d '{ "show_name": "Harry Potter patched", "show_date": "2020-05-06" }'`

```json
{
  "show": {
    "id": 3,
    "show_date": "Wed, 06 May 2020 00:00:00 GMT",
    "show_name": "Natasha romanov patched"
  },
  "success": true
}
```

#### DELETE /shows/<int:id\>

- General:

  - Deletes a shows by id form the url parameter.
  - Roles authorized :  Producer.

- Sample: `curl http://127.0.0.1:5000/shows/3 -X DELETE`

```json
{
  "message": "show id 3, named Harry Potter patched was deleted",
  "success": true
}
```

#### GET /magicians

- General:

  - Returns all the magicians.
  - Roles authorized :  Assistant, Director, Producer.

- Sample: `curl http://127.0.0.1:5000/magicians`

```json
{
  "magicians": [
    {
      "age": 20,
      "gender": "male",
      "id": 1,
      "name": "Harry Potter"
    },
    {
      "age": 50,
      "gender": "male",
      "id": 2,
      "name": "Dumbledore"
    }
  ],
  "success": true
}
```

#### GET /magicians/\<int:id\>

- General:

  - Route for getting a specific magician.
  - Roles authorized :  Assistant, Director, Producer.

- Sample: `curl http://127.0.0.1:5000/magicians/1`

```json
{
  "magician": {
    "age": 20,
    "gender": "male",
    "id": 1,
    "name": "Harry Potter"
  },
  "success": true
}
```

#### POST /magicians

- General:

  - Creates a new magician based on a payload.
  - Roles authorized : Director, Producer.

- Sample: `curl http://127.0.0.1:5000/magicians -X POST -H "Content-Type: application/json" -d '{ "name": "Lisa", "age": 32, "gender": "female" }'`

```json
{
  "magician": {
    "age": 32,
    "gender": "female",
    "id": 3,
    "name": "Lisa"
  },
  "success": true
}
```

#### PATCH /magicians/\<int:id\>

- General:

  - Patches an magician based on a payload.
  - Roles authorized : Director, Producer.

- Sample: `curl http://127.0.0.1:5000/magicians/3 -X POST -H "Content-Type: application/json" -d '{ "name": "Lisa", "age": 22, "gender": "female" }'`

```json
{
  "magician": {
    "age": 22,
    "gender": "female",
    "id": 3,
    "name": "Lisa"
  },
  "success": true
}
```

#### DELETE /magicians/<int:id\>

- General:

  - Deletes an magician by id form the url parameter.
  - Roles authorized : Director, Producer.

- Sample: `curl http://127.0.0.1:5000/magicians/3 -X DELETE`

```json
{
  "message": "magician id 3, named Lisa was deleted",
  "success": true
}
```

## Project dependencies

## Getting Started

#### Installing Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup

The project uses Postgresql as its database, you would need to create one locally and reflect it in setup.sh.
To update the database and seed run the following :

```bash
python manage.py db upgrade
python manage.py seed
```

- you may need to change the database url in setup.sh after which you can run

```bash
source setup.sh
```

- Start server by running

```bash
flask run
```

## Testing

For testing locally, we need to reset database.
To reset database, run

```
python manage.py db downgrade
python manage.py db upgrade
python manage.py seed
```

### Error Handling

- 403 errors due to RBAC are returned as

```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

Other Errors are returned in the following json format:

```json
{
  "success": "False",
  "error": 422,
  "message": "Unprocessable entity"
}
```

The error codes currently returned are:

- 400 – bad request
- 403 – unauthorized
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error
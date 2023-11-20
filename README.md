[![Checks](https://github.com/MohammedSaLah-Eldeen/recipe-app-api/actions/workflows/checks.yml/badge.svg)](https://github.com/MohammedSaLah-Eldeen/recipe-app-api/actions/workflows/checks.yml)

# recipe-app-api
Recipe API App. Fully functional backend API that could be used with a frontend to create a recipe app or a website

## Implmentation
Docker Containers were used mainly in the development along with docker compose to building the app starting it and such on. <br>
PostgreSQL is the default database for this project instead of sqlite that comes as a default with django <br>.

* to build the application `docker compose build`
* to run the application `docker compose up`
* to run a specifc command, `docker compose run --rm app sh -c "HERE GOES THE COMMAND"`
the --rm will make sure to remove the container after the command has been executed. <br>

check
* `Dockerfile`
* `docker-compose.yml`
to understand more about how the image was built and the different used services in docker compose.

### Apps
This API consists of 3 main Apps: <br>

#### core
features but limited to:
* the management command `wait_for_db` that checks whether database container is running to start the connection.
* a custom user model. 
* a custom admin interface for the User model.
* all used database models for this API.
* all database models tests functionality.

#### user
features but limited to:
* uses API tokens to handle Authentication with the help of the django rest franework `ObtainAuthToken` class that uses the `AuthTokenSerializer` for serialization.
* uses django rest framework `generics.CreateAPIView` to accept POST requests for signing up with the correct input information uses the `UserSerializer` with the help of the django rest framework `ModelSerializer`.
* also users can view and update their information with the `ManageUserView` that uses `generics.RetrieveUpdateAPIView` to allow for GET, PUT and PATCH requests, still uses the `UserSerializer`.

## API DOCS
Head to /api/docs to view the Swagger API Documentation, <br>
you can find all the available endpoints to use and test the API

### Enjoy :)

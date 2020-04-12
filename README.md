Casting Agency
-----

### Introduction
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies

### Overview

This is just an api. No client has been implemented yet.
This app allows users to
* add, update and delete actors,
* add, update and delete movies
* assign actors to movies via movie sets (an actor can belong to more than one movie set and so does a movie)

### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  └── auth
      ├── auth *** responsible to validating user tokens
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* auth functions are located in auth.py
* manage.py can be used to create and run migrations


USER ROLES AND PERMISSIONS
-----
There are three types of users in this project
1. Casting Assistant (Can view actors and movies)
2. Casting Director
   * All permissions a Casting Assistant has and…
   * Add or delete an actor from the database
   * Modify actors or movies
3. Executive Producer
   * All permissions a Casting Director has and…
   * Add or delete a movie from the database


### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Run Migrations 
```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/ 
  $ python manage.py db init
  $ python manage.py db migrate
  $ python manage.py db upgrade
  ```
### Making API calls
   To start making API calls with sample tokens

1. Get authorization url
  ```http://localhost:5000/authorization/url
  ```
  Paster the url in the browser and follow the instructions below
2. Get token 
    For testing sake, I created three test users with the following info
    Casting Assistant
      * username casting-assistant@gmail.com
      * password New_movie_user_2019
    Casting Director
      * username casting-director@gmail.com
      * password New_movie_user_2019
    Executive Producer
       * username casting-director@gmail.com
       * password New_movie_user_2019
3. Get the token from the browser redirect after logging in with one of these users
   This depends on the action you want to perform
4. Use postman or any package to make a request with bearer authorization header

## Running Tests
   Tests currently use a sample Casting Director token that has all roles
   although others are used to satisfy specific 401 test cases
   These tokens do expire so to make sure tests aree not failing beause of this,
   follow the steps to get tokens above and update EXECUTIVE_PRODUCER_TOKEN in the tests.py
   
   
## Testing the live app
   1. production url 
    ```http://localhost:5000/authorization/url
    ```
   2. Test instructions
      Test your endpoints with [Postman](https://getpostman.com). 
      - get an authorization url **https://udacity-movies-app-fsnd.herokuapp.com/**
      - login with one of the users specified in **2. Get token**
      - Import the postman collection `./starter/casting_gency_postman_collection.json`
      - use the token above to test the endpoints (take note of user permissions as listed above)
     
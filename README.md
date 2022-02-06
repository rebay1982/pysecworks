# pysecworks

## Basic Setup and installation
1. `python -m venv venv`
2. `. ./venv/bin/activate`
3. `pip install -r requirements.txt`

## Get The project running
`flash run` at the root.

## Operating Manual
### Retrieve a token for the API
`curl -u <user>:<password> -XPOST "http://<ip>:<port>/graphql/tokens"`

### Query API
`curl -X<method> "http://<ip>:<port>/graphql" -H "Authorization:Bearer <token>"`

# TODO: DOCUMENT API




### Database migration
1. `flask db migrate`  -- The initial users table migration. 
2. `flask db upgrade` -- Runs the configured migration against the db.

## Choice of Frameworks and Libraries

### Web
I hope I made the right choice as I start my first web project in Python ;) 

I have used this post as reference to make my decision:
[Flask vs Django](https://hackr.io/blog/flask-vs-django).

#### Flask
I have chosen to go with Flask as I'm new to writing web applications using 
python. The project seems relatively simple and lightweight with some basic 
features. SQL integration with the data base will also be relatively simple.

Essentially, Flask seems to provide basic functionality and gives the
flexibility to use different libraries to extend its functionality.

The tutorial used for the majority of this project to get up and running can 
be found [here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

#### Django
The other contender was Django which seems to be a lot more complete from a 
feature set perspective but potentially excessive for this small project. Let's
start small and evolve from there.

### Security / Authentication and Authorization

#### werkzeug
Werkzeug is used to hash (with a salt) passwords and allows for validating that
a specific password, matches a certain hash. This way we can securely store the
hashed password for users and easily validate if the provided password matches
the stored hash.

#### Flask-HTTPAuth
Library used to implement API authentication so that users of the API can
provide a username and password to authenticate to the API. Following that, they
can request a token and use it until it expires to make subsequent calls to the 
API.

### Misc

#### python-dotenv
Simply to set basic environment variables for Flask.


### Database

#### Flask-Migrate
Maybe overkill for a small project like this, but I always love having options
to allow for database schema migrations. I can become handy for maintenance 
purposes down the road. 

It's a little price to pay now for and cheap compared to having to add this at 
a future date.

#### Flask-SQLAlchemy
SQLAlchemy seems to be a popular ORM choice for Python and I went for it. The 
reason for the ORM is that I want to avoid using raw SQL for this basic project
and shield against mistakes I might make that would allow for SQL Injection 
attacks.


## Misc notes
Check Tutorials:
1. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
2. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
3. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xix-deployment-on-docker-containers
4. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis

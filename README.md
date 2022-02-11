# pysecworks

Greetings!

Welcome to pysecworks, an application/project I put together as a first Python project. The
objective was to put together a simple application that implements rudamentary features such as API
authentication, token creation and revokation, a GraphQL API, and essentially basic CRUD operations.

## Getting Started

### Basic Setup and Installation
In the project's root, run the following:

1. `python -m venv venv`
2. `. ./venv/bin/activate`
3. `pip install -r requirements.txt`

### Get the Project Running
After installing all dependencies, run the following command from the project root:

`flash run`

## Docker

You can run the project from a docker container. First, you will need to build the image. From
there, you have multiple options to run it. All these steps are described in the following sections.

### Building the Image
You can build the image using the following command on Linux.

`sudo docker build -t pysecworks:latest .`

### Running the Container
You can specify the "PORT" environement variable to have the service start on a specific port.
Omiting this configuration runs the application on the default port: 5000.

Example: Run the service using the default port.
`sudo docker run --name pysecworks --network host -d --rm pysecworks:latest`

Example: Run the service on port 8000.
`sudo docker run --name pysecworks --network host -d -e PORT=8000 --rm pysecworks:latest`


## Using the Application and API
### Authentication
The API has multiple endpoints. The first step you need to do is authenticate to it and retrieve a
valid token. This token will be required to access the GraphQL API.

`curl -u <user>:<password> -XPOST "http://localhost:<port>/graphql/tokens"`

The default user name and password are `secureworks`, `supersecret`. You will be provided a token
that expires one hour from the time it was created.

For security reasons, you can revoke and invalidate the token with the following command:
`curl -XDELETE "http://localhost:<ip>/graphql/tokens" -H "Authorization: Bearer <token>"`

### GraphQL API
The GraphQL API provides a way to look up IP addresses against spamhause.org. The reponse codes
that are returned are documented [here](https://www.spamhaus.org/faq/section/DNSBL%20Usage#200)

The endpoint is under `/graphql`.

#### Query
To retrieve details related to an IP, send in a `getIpDetails` request with an IP as a parameter.
You can request the following fields:

```
  uuid          -> a unique identifier for the entry.
  created_at    -> the time (UTC) at which the entry was looked up for the first time.
  updated_at    -> the time (UTC) at which the entry was last looked up.
  response_code -> the latest reponse codes received from spaumhaus at the last update.
  ip_address    -> the IP address associated with this record.
```

Here is an example:
```
curl -vvv -XPOST "http://localhost:<port>/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization:Bearer <token>" \
  -d '{ \
        "query":"query { \
          getIpDetails(ip: \"127.0.0.1\") { \
            uuid created_at updated_at response_code ip_address \
          } \
        }" \
      }'
```

#### Mutation
Mutations allow you to `enqueue` lookup jobs. Essentially, you pass this endpoint an array of IP 
addresses you with to have looked up against `spamhaus.org`.

Here's how to do it:
```
curl -vvv -XPOST "http://localhost:<port>/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization:Bearer <token>" \
  -d '{ \
        "query":"mutation { \
          enqueue(ip: [\"1.0.0.1\",\"127.0.0.2\"]) \
        }" \ 
      }'
```

This endpoint will return the number of IP addresses that were enqueues for the request.

### Database Migration
The database has already been migrated, but you can delete the `app.db` file and start from scratch
using the following command:

1. `flask db migrate` -- The initial users table migration. 
2. `flask db upgrade` -- Runs the configured migration against the db.

## Project Structure
Being my first Python project, I tried to familiarize myself with best practices for Python
projects. Here's how I broke everything down and where everything is.

```
▾ app/                ; Application root
  ▾ api/              ; API, everything related to the API (REST and GraphQL)
      __init__.py
      auth.py         ; Authentication endpoints
      errors.py       ; API/Web error handling.
      graphql.py      ; The GraphQL endpoint + resolvers
      schema.py       ; The GraphQL schemas
      tokens.py       ; Token API
    __init__.py
    lookup.py         ; Lookup -- everything related to the lookup code against spamhaus.org
    models.py         ; All the models the application uses
▸ migrations/
  .env
  .flaskenv           ; Test environment variable file
  app.db              ; SQLite application database
  config.py           ; Basic configurtion file for the application
  Dockerfile          ; The Dockerfile to build the container image
  entrypoint.sh       ; The startup script for the docker container
  pysecworks.py       ; The application
  README.md           ; This file ;)
  requirements.txt    ; Requirements file for pip install
  tests.py            ; Unit tests
```


## Choice of Frameworks and Libraries
This section describes the choices that were made with regards to the different libraries used.

### Web
Being new to Python I relied a lot on a few blog posts to make my initial choice for a web
framework.

I have used this post as reference to make my decision:
[Flask vs Django](https://hackr.io/blog/flask-vs-django).

#### Flask
I have chosen to go with Flask as I'm new to writing web applications using Python. The project 
seems relatively simple and lightweight with some basic features. SQL integration with the data base
will also be relatively simple.

Essentially, Flask seems to provide basic functionality and gives the flexibility to use different
libraries to extend its functionality. This is appealing (to me, anyway) as I have a preference to
start small and build things up when I'm in unfamiliar terriroty.

The tutorial used for the majority of this project to get up and running can be found
[here](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

#### Django
The other contender was Django which seems to be a lot more complete from a feature set perspective
but potentially excessive for this small project. I wanted to avoid overwhelming myself with a
larger framework.

#### Ariadne
Not having done any GraphQL in the past, I found it intriguing to go with a  "schema-first"
approach. Not going to create a debate over "schema-first" or "code-first" and which is better but
that is how we've been building APIs where I work. We write an OpenAPI specification provide those
specifications to our clients. We then generate code off of that OpenAPI specification (still qwerky
and needs some adjustments here and there). This is why I chose to try out "schema-first" for my
first GraphQL API.

This [blog](https://blog.logrocket.com/build-graphql-api-python-flask-ariadne/) has proven to be
pretty helpful too.

### Security / Authentication and Authorization

#### werkzeug
Werkzeug is used to hash (with a salt) passwords and allows for validating that a specific password,
matches a certain hash. This way we can securely store the hashed password for users and easily 
validate if the provided password matches the stored hash.

#### Flask-HTTPAuth
Library used to implement API authentication so that users of the API can provide a username and 
password to authenticate to the API. Following that, they can request a token and use it until it 
expires to make subsequent calls to the API.

### Misc

#### python-dotenv
Simply to set basic environment variables for Flask.

#### dnspython
Simple library to do DNS lookups with Python. The main back bone for doing the look ups against
spamhaus.org

#### gunivorn
Needed a "production" ready WSGI HTTP server. This is what was used in the blog I was following to
learn building a web service with Python. 

### Database

#### Flask-Migrate
Maybe overkill for a small project like this, but I always love having options to allow for database
schema migrations. It can become handy for maintenance purposes down the road. 

It's a little price to pay now for and cheap compared to having to add this at a future date.

#### Flask-SQLAlchemy
SQLAlchemy seems to be a popular ORM choice for Python and I went for it. The reason for the ORM 
is that I want to avoid using raw SQL for this basic project and shield against mistakes I might 
make that would allow for SQL Injection attacks. Also simplifies interaction with the database.

## What Could Have Been Better

The job queue. I implemented it with a simple thread. The thread picks up the `enqueue` request and
runs the look up on a background thread, releasing the application thread to return to the client.

This "does the job" but wasn't what I was intending initially. My primary idea would have been 
having a thread pool of workers and have the application thread enqueue a lookup job in a
synchronized queue. From there, a worker thread would pick it up and do the look up, updating the 
database if needed.

The problem I was having is that I wasn't able to provide a correct application context to the
worker threads.

```
class LookupQueue(Queue):
    def __init__(self, nb_workers = 1):
        Queue.__init__(self)
        self.nb_workers = nb_workers
        self.start_workers()

    def add_lookup(self, ips):
        self.put(ips)

    def start_workers(self):
        for i in range(self.nb_workers):
            t = Thread(target = self.worker, args=(self, current_app._get_current_object()))
            t.daemon = True
            t.start()

    def worker(self, app):
        while True:
            ips = self.get()
            with app.app_context():
                lookup_worker(ips)
            self.task_done()
```

I unfortunately ran out of spare time to work on this project but it will be something I will be
looking forward in picking up again and improving.

I know I could have implemented it with Redis Queues, but that seemed over complicated for this 
simple use case.

## Misc Notes

### Tutorials
1. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
2. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
3. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xix-deployment-on-docker-containers
4. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis

### Spamhaus Usage
```
$ dig +short <reverse_ip>.zen.spamhaus.org
```
Good examples are `1.0.0.127.zen.spamhaus.org` and `2.0.0.127.zen.spamhaus.org`


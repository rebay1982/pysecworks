# pysecworks

## Basic Setup and installation
1. `python -m venv <virtual_env>`
2. `. ./<virtual_env>/bin/activate`
3. `pip install -r requirements.txt`

## Get The project running
`flash run` at the root.


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

### Misc

#### python-dotenv
Simply to set basic environment variables for Flask.



## Misc notes
Check Tutorials:
1. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
2. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
3. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xix-deployment-on-docker-containers
4. https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis

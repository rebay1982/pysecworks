from app import app

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/graphql')
def graphql():
    return "Hello, GraphQL!"

@app.route('/login')
def login():
    return app.config['DB_USERNAME'] + ':' + \
        app.config['DB_PASSWORD'] + '\r\n' + \
        'Secret Key: ' + app.config["SECRET_KEY"]

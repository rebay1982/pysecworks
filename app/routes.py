from app import app

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/graphql')
def graphql():
    return "Hello, GraphQL!"

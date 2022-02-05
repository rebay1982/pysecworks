from app.api import bp

@bp.route('/')
def graphql():
    return "Hello, GraphQL!"



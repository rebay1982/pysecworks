# AIP Sauce
from app.api import bp
from app.api.auth import token_auth

@bp.route('')
@token_auth.login_required
def graphql():
    return "Hello, GraphQL!"

#@bp.route('mutate')
#def mutation():





import logging
from app.api import bp
from app.api.auth import token_auth
from app.api.schema import type_defs, query, mutation
from app.lookup import lookup_worker 
from app.models import Lookup

from flask import request, jsonify
from ariadne import graphql_sync, make_executable_schema

@bp.route('', methods=['GET'])
@token_auth.login_required
def graphql_get():
    return "Hello, GraphQL!"

@bp.route('', methods=['POST'])
@token_auth.login_required
def graphql_post():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value={"request": request})
    status_code = 200 if success else 400
    return jsonify(result), status_code

@query.field("getIpDetails")
def resolve_getipdetails(_, info, ip):
    lookup = Lookup.get(ip)
    if lookup is not None:
        return lookup.to_dict()
    
    return Lookup(response_code="No records found.", ip_address=ip).to_dict()

@mutation.field("enqueue")
def resolve_enqueue(_, info, ip):
    lookup_worker(ip)
    return len(ip)

schema = make_executable_schema(type_defs, [query, mutation])



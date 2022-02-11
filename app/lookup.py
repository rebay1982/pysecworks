import ipaddress
import socket
import dns.resolver

from app import db
from threading import Thread

from app.models import Lookup
from flask import current_app

def exec_lookup(ips):
    Thread(target=lookup_worker, args=(current_app._get_current_object(), ips)).start()

def lookup_worker(app, ips):
    with app.app_context():
        for ip in ips:
            # Skip if the IP is not valid.
            if is_valid_ip(ip):
                lookup = "{}.zen.spamhaus.org".format(reverse_ip(ip))
                response_code = get_lookup_response_code(lookup)
                
                # Get the lookup record from DB.
                lookup = Lookup.get(ip) 
                if lookup is None:
                    Lookup.create_new(ip, response_code)
                else:
                    lookup.update(response_code)
                
                db.session.commit()

# Function to quickly validate if a string represents a valid IPv4 address.
def is_valid_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False

# Function that takes a string representing a valid IPv4 address and reverses
# all the octets.
def reverse_ip(ip):
    tokenized = ip.split('.')
    rev_ip = "{}.{}.{}.{}".format( \
        tokenized[3], tokenized[2], tokenized[1], tokenized[0])
     
    return rev_ip

# Function that does the look up of a specific name and returns the response
#   code for it. If multiple 
def get_lookup_response_code(lookup):
    response_code = ""
    try:
        responses = dns.resolver.resolve(lookup)
        nb_responses = len(responses)
        for i in range(nb_responses):
            response_code += str(responses[i])
            if i < (nb_responses - 1):
                response_code += ", "
    
    except dns.resolver.NXDOMAIN:
        response_code = "No Response"

    return response_code


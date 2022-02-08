from ariadne import gql, QueryType, MutationType

type_defs = gql(
    """
    type Query {
        getIpDetails(ip: String!): Lookup
    }

    type Lookup {
        uuid: ID
        created_at: String 
        updated_at: String
        response_code: String!
        ip_address: String!
    }

    type Mutation {
        enqueue(ip: [String!]!): Int
    }
    """
)

query = QueryType()
mutation = MutationType()



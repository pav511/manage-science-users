# manage-science-users

## build and run container

` docker build -t manage-science-users-image . ` <br />
`docker run -r MONGODB_URL=${MONGODB_URL} -p 8000:8000 manage-science-users-image:latest ` <br />
view at: http://localhost:8000/graphql


## Info

manage-science-users is a microservice that runs in a docker container that serves graphql [https://graphql.org/] queries to a database backend to manage user data.
  The service is written in python3 [https://www.python.org/] and uses strawberry [https://strawberry.rocks/] to communicate with a mongoDB database [https://www.mongodb.com/] <br />
  
In main.py the Mutation class holds a variety of functions responsible for inserting, and modifying entries in the database.
The Query class provides a resolver for obtaining data from the database.

The application uses pymongo as a driver to communicate with the backend database. Database user access management is provided by mongoDB and authenticated with a URI used to connect with a mongoDB deployment.
The URI takes the form:
` mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]] `
and is stored as an environment variable. To avoid distributing database access, the environment variable is passed to the docker container at runtime with
flag ` -e MONGODB_URL=${MONGODB_URL} `
  
GraphQL query to update recent_activity in backend database. Implementation for update is in update_scienceUser_status_activity in the Mutation class.
```
mutation MyMutation {
  __typename
  updateScienceuserStatusActivity(uid: "wns") {
    status {
      lastAccountActivity
    }
  }
}
```
strawberry library does not provide built in authentication, but provides Permission classes to process domain-specific authentication logic. For this setup, this may involve verifying database access with MongoDB directly using the pymongo python driver. An alternative would be allowing graphQL to handle authentication by writing resolvers to process user data and permissions.

An alternative technology would be to use fastapi [https://fastapi.tiangolo.com/] along with motor driver [https://www.mongodb.com/docs/drivers/motor/] to communicate with the mongoDB. Fastapi has the advantage of having built in authentication.
Database alternative could be postgesql [https://www.postgresql.org/] for a relational database vs a document database.




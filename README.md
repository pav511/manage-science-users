# manage-science-users

build and run container

docker build -t manage-science-users-image .
docker run -r MONGODB_URL=${MONGODB_URL} -p 8000:8000 manage-science-users-image:latest

view at:
http://localhost:8000/graphql

GraphQL recent_activity query

mutation MyMutation {
  __typename
  updateScienceuserStatusActivity(uid: "wns") {
    status {
      lastAccountActivity
    }
  }
}

Database authentication is manged by MongoDB and URL environment variable passed to container through docker run
Strawberry does not support built in authentication but provides permission classes for domain specific authentication
to be implemented by the developer.



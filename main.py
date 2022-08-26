import os
import strawberry
import typing
import pymongo
from pymongo import MongoClient
import zulu


def get_database():
    CONNECTION_STRING = os.environ["MONGODB_URL"]
    client = MongoClient(CONNECTION_STRING)
    dbname = client["science_users"]
    collection_name = dbname["science_users_info"]
    return collection_name


@strawberry.type
class Status:
    training_uptodate: bool
    last_account_activity: str


@strawberry.type
class ScienceUser:
    uid: str
    gecos: str
    uidNumber: int
    eppns: typing.List[str]
    status: "Status"
    

def get_scienceUsers():
    collection = get_database()
    item_details = collection.find() 
    scienceUsers = list()
    for x in item_details:
        scienceUsers.append(ScienceUser(x["uid"], x["gecos"], x["uidNumber"], x["eppns"], Status(x["status"].get("training_uptodate"), x["status"].get("last_account_activity"))))
        print(x)
    return scienceUsers


@strawberry.type
class Query:
    scienceUsers: typing.List[ScienceUser] = strawberry.field(resolver=get_scienceUsers)
    #statuses: typing.List[Status] = strawberry.field(resolver=get_statuses)

@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_scienceUser(self, uid: str, gecos: str, uidNumber: int, eppns: typing.List[str], training_uptodate: bool, last_account_activity: str) -> ScienceUser:
        print(f'Adding {uid}')
        eppns = eppns[0].split(' ') # flatten into proper list, since all elements at index 0.
        # bundle status object
        status = Status(training_uptodate=training_uptodate, last_account_activity=last_account_activity)
        collection = get_database()
        collection.insert_one({"uid":uid, "gecos":gecos, "uidNumber":uidNumber, "eppns":eppns, "status":{"training_uptodate":training_uptodate, "last_account_activity":last_account_activity}})
        new_scienceUser = ScienceUser(uid=uid, gecos=gecos, uidNumber=uidNumber, eppns=eppns, status=status)
        return new_scienceUser


    @strawberry.mutation
    def update_scienceUser_uid(self, uid: str, new_uid: str) -> ScienceUser:
        print(f'Changing {uid} to {new_uid}')
        collection = get_database()
        item_details = collection.update_one({"uid":uid}, {"$set": {"uid":new_uid}})
        x = collection.find_one({"uid":new_uid})
        return ScienceUser(uid=new_uid, gecos=x["gecos"], uidNumber=x["uidNumber"], eppns=x["eppns"], status=Status(x["status"].get("training_uptodate"), x["status"].get("last_account_activity")))
        

    @strawberry.mutation
    def update_scienceUser_gecos(self, gecos: str, new_gecos: str) -> ScienceUser:
        print(f'Changing {gecos} to {new_gecos}')
        collection = get_database()
        item_details = collection.update_one({"gecos":gecos}, {"$set": {"gecos":new_gecos}})
        x = collection.find_one({"gecos":new_gecos})
        return ScienceUser(uid=x["uid"], gecos=new_gecos, uidNumber=x["uidNumber"], eppns=x["eppns"], status=Status(x["status"].get("training_uptodate"), x["status"].get("last_account_activity")))


    @strawberry.mutation
    def update_scienceUser_uidNumber(self, uidNumber: int, new_uidNumber: int) -> ScienceUser:
        print(f'Changing {uidNumber} to {new_uidNumber}')
        collection = get_database()
        item_details = collection.update_one({"uidNumber":uidNumber}, {"$set": {"uidNumber":new_uidNumber}})
        x = collection.find_one({"uidNumber":new_uidNumber})
        return ScienceUser(uid=x["uid"], gecos=x["gecos"], uidNumber=new_uidNumber, eppns=x["eppns"], status=Status(x["status"].get("training_uptodate"), x["status"].get("last_account_activity")))


    @strawberry.mutation
    def update_scienceUser_eppns(self, uidNumber: int, eppns: str, new_eppns: str) -> ScienceUser:
        print(f'Changing {eppns} to {new_eppns}')
        collection = get_database()
        item_details = collection.find_one({"uidNumber":uidNumber});
        eppns_field = item_details["eppns"]
        eppns_field = [w.replace(eppns, new_eppns) for w in eppns_field]
        collection.update_one({"uidNumber":uidNumber}, {"$set": {"eppns":eppns_field}})
        x = collection.find_one({"uidNumber":uidNumber})
        return ScienceUser(uid=x["uid"], gecos=x["gecos"], uidNumber=x["uidNumber"], eppns=eppns_field, status=Status(x["status"].get("training_uptodate"), x["status"].get("last_account_activity")))


    @strawberry.mutation
    def update_scienceUser_status_training(self, uidNumber: int, new_training: bool) -> ScienceUser:
        print(f'Changing training_uptodate to {new_training}')
        collection = get_database()
        item_details = collection.find_one({"uidNumber":uidNumber});
        status_field = item_details["status"]
        status_field["training_uptodate"] = new_training
        collection.update_one({"uidNumber":uidNumber}, {"$set": {"status":status_field}})
        x = collection.find_one({"uidNumber":uidNumber})
        return ScienceUser(uid=x["uid"], gecos=x["gecos"], uidNumber=x["uidNumber"], eppns=x["eppns"], status=Status(x["status"].get("training_uptodate"), x["status"].get("last_account_activity")))
        

    @strawberry.mutation
    def update_scienceUser_status_activity(self, uid: str) -> ScienceUser:
        print(f'Changing last_account_activity to current time')
        collection = get_database()
        item_details = collection.find_one({"uid":uid});
        status_field = item_details["status"]
        status_field["last_account_activity"] = zulu.now().format()
        collection.update_one({"uid":uid}, {"$set": {"status":status_field}})
        x = collection.find_one({"uid":uid})
        return ScienceUser(uid=x["uid"], gecos=x["gecos"], uidNumber=x["uidNumber"], eppns=x["eppns"], status=Status(x["status"].get("training_uptodate"), x["status"].get("last_account_activity")))
        

schema = strawberry.Schema(query=Query, mutation=Mutation)



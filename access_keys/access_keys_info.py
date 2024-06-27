import boto3
from datetime import datetime
from dateutil.tz import tzutc
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-a", "--active", help="list active keys only", action="store_true")
parser.add_argument("-i", "--inactive", help="list inactive keys only", action="store_true")
parser.add_argument("-d", "--days", help="list keys older than N days", type=int)
args = parser.parse_args()

client = boto3.client("iam")


def calculate_age(create_date):
    current_date = datetime.now(tzutc())
    age = current_date - create_date
    return age.days


for user in client.list_users()["Users"]:
    access_key_users = client.list_access_keys(UserName=user["UserName"])["AccessKeyMetadata"]
    for key in access_key_users:
        create_date = key["CreateDate"]
        age = calculate_age(create_date)
        if args.days and age < args.days:
            continue
        if args.active and key["Status"] == "Inactive":
            continue
        if args.inactive and key["Status"] == "Active":
            continue
        print(user["UserName"], key["AccessKeyId"], key["Status"], age)
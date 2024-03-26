#!/usr/bin/env python3

# Get current running instance's types, platform, and total RI normalized units.

import boto3


ec2 = boto3.client("ec2")


def get_total_units(instance_type):
    if ".nano" in instance_type:
        units = 0.25
    elif ".micro" in instance_type:
        units = 0.5
    elif ".small" in instance_type:
        units = 1
    elif ".medium" in instance_type:
        units = 2
    elif ".large" in instance_type:
        units = 4
    elif ".xlarge" in instance_type:
        units = 8
    elif ".2xlarge" in instance_type:
        units = 16
    elif ".3xlarge" in instance_type:
        units = 24
    elif ".4xlarge" in instance_type:
        units = 32
    elif ".6xlarge" in instance_type:
        units = 48
    elif ".8xlarge" in instance_type:
        units = 64
    elif ".9xlarge" in instance_type:
        units = 72
    elif ".10xlarge" in instance_type:
        units = 80
    elif ".12xlarge" in instance_type:
        units = 96
    elif ".16xlarge" in instance_type:
        units = 128
    elif ".18xlarge" in instance_type:
        units = 144
    elif ".24xlarge" in instance_type:
        units = 192
    elif "32xlarge" in instance_type:
        units = 256
    elif "48xlarge" in instance_type:
        units = 384
    elif "56xlarge" in instance_type:
        units = 448
    elif "112xlarge" in instance_type:
        units = 896
    else:
        units = 0

    return units


def describe_instance_types():
    response = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    instances = response["Reservations"]
    instance_data = {}

    for reservation in instances:
        for instance in reservation["Instances"]:
            platform = instance["PlatformDetails"]
            instance_type = instance["InstanceType"]
            if platform not in instance_data:
                instance_data[platform] = {}
            if instance_type not in instance_data[platform]:
                instance_data[platform][instance_type] = {}
                instance_data[platform][instance_type]["count"] = 1
                instance_data[platform][instance_type]["units"] = get_total_units(instance_type)
                instance_data[platform][instance_type]["family"] = instance_type.split(".")[0]
                instance_data[platform][instance_type]["total_units"] = 0
            else:
                instance_data[platform][instance_type]["count"] += 1

    for platform in instance_data:
        for instance_type in instance_data[platform]:
            total_units = (
                instance_data[platform][instance_type]["units"]
                * instance_data[platform][instance_type]["count"]
            )
            instance_data[platform][instance_type]["total_units"] = int(total_units)

    return instance_data


def create_csv():
    with open("instance_data.csv", "w") as file:
        file.write("Platform,Instance Type,Count,Units,Family,Total Units\n")
        instance_data = describe_instance_types()
        for platform in instance_data:
            for instance_type in instance_data[platform]:
                file.write(
                    f"{platform},{instance_type},{instance_data[platform][instance_type]['count']},{instance_data[platform][instance_type]['units']},{instance_data[platform][instance_type]['family']},{instance_data[platform][instance_type]['total_units']}\n"
                )


if __name__ == "__main__":
    create_csv()
    instance_data = describe_instance_types()
    for i in instance_data:
        print(i)
        for j in instance_data[i]:
            print(j, instance_data[i][j])

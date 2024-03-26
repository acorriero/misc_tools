#!/usr/bin/env python3

import boto3

# Get current RI details.

ec2 = boto3.client("ec2")


def get_normalized_units(instance_type):
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


def describe_reserved_instances():
    response = ec2.describe_reserved_instances()
    instances = response["ReservedInstances"]

    value = []

    for instance in instances:
        instance_type = instance["InstanceType"]
        instance_count = instance["InstanceCount"]
        product_description = instance["ProductDescription"]
        state = instance["State"]
        instance_family = instance_type.split(".")[0]

        units = get_normalized_units(instance_type)

        normalized_units = units * instance_count

        if state == "active":
            value.append(
                {
                    "instance_type": instance_type,
                    "instance_count": instance_count,
                    "product_description": product_description,
                    "instance_family": instance_family,
                    "units": units,
                    "normalized_units": normalized_units,
                }
            )

    return value


def sort_dri(dri):
    sorted_dri = {}
    for i in dri:
        if i["product_description"] not in sorted_dri:
            sorted_dri[i["product_description"]] = {}
        if i["instance_type"] not in sorted_dri[i["product_description"]]:
            sorted_dri[i["product_description"]][i["instance_type"]] = {}
            sorted_dri[i["product_description"]][i["instance_type"]]["count"] = i["instance_count"]
            sorted_dri[i["product_description"]][i["instance_type"]]["units"] = i["units"]
            sorted_dri[i["product_description"]][i["instance_type"]]["family"] = i["instance_family"]
            sorted_dri[i["product_description"]][i["instance_type"]]["total_units"] = int(i["normalized_units"])
        else:
            sorted_dri[i["product_description"]][i["instance_type"]]["count"] += i["instance_count"]
            sorted_dri[i["product_description"]][i["instance_type"]]["units"] = i["units"]
            sorted_dri[i["product_description"]][i["instance_type"]]["family"] = i["instance_family"]
            sorted_dri[i["product_description"]][i["instance_type"]]["total_units"] += int(i["normalized_units"])

    return sorted_dri


def create_csv():
    with open("ri_details.csv", "w") as f:
        f.write("Platform,Instance Type,Count,Units,Family,Total Units\n")
        sorted_dri = sort_dri(describe_reserved_instances())
        for i in sorted_dri:
            for j in sorted_dri[i]:
                f.write(
                    f"{i},{j},{sorted_dri[i][j]['count']},{sorted_dri[i][j]['units']},{sorted_dri[i][j]['family']},{sorted_dri[i][j]['total_units']}\n"
                )


if __name__ == "__main__":
    create_csv()
    sorted_dri = sort_dri(describe_reserved_instances())

    for i in sorted_dri:
        print(i)
        for j in sorted_dri[i]:
            print(j, sorted_dri[i][j])

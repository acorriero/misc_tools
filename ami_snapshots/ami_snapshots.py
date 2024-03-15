#!/usr/bin/env python3

import boto3
import re
import csv

ec2 = boto3.client("ec2")


def get_ami_ids_from_snapshots():
    response = ec2.describe_snapshots(
        Filters=[{"Name": "description", "Values": ["*for ami-*"]}], OwnerIds=["self"]
    )
    snapshot_data = {}
    snapshots = response["Snapshots"]

    for snapshot in snapshots:
        snapshot_id = snapshot["SnapshotId"]
        ami_id = snapshot["Description"].split(" ")[4]
        instance_id = re.search(r"\((.*?)\)", snapshot["Description"]).group(1)
        start_time = str(snapshot["StartTime"])
        volume_size = str(snapshot["VolumeSize"])
        if "Tags" in snapshot:
            for tag in snapshot["Tags"]:
                if tag["Key"] == "Name":
                    snapshot_name = tag["Value"]
                else:
                    snapshot_name = "No Name"
                    continue
        else:
            snapshot_name = "No Name"

        if snapshot_id not in snapshot_data:
            snapshot_data[snapshot_id] = (
                snapshot_name,
                start_time,
                volume_size,
                ami_id,
                instance_id,
            )
        
        else:
            snapshot_data[snapshot_id] = (
                snapshot_name,
                start_time,
                volume_size,
                ami_id,
                instance_id,
            )


    return snapshot_data


def get_existing_ami_ids():
    response = ec2.describe_images(Owners=["self"])
    return [image["ImageId"] for image in response["Images"]]


def main():
    snapshot_ids = get_ami_ids_from_snapshots()
    existing_ami_ids = get_existing_ami_ids()
    with open("ami_snapshots.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Snapshot ID",
                "Snapshot Name",
                "Started At",
                "Size",
                "AMI ID",
                "Instance ID",
            ]
        )
        
        for snapshot_id, snapshot_data in snapshot_ids.items():
            if snapshot_data[3] not in existing_ami_ids:
                writer.writerow(
                    [
                        snapshot_id,
                        snapshot_data[0],
                        snapshot_data[1],
                        snapshot_data[2],
                        snapshot_data[3],
                        snapshot_data[4],
                    ]
                )
            else:
                continue


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import boto3
import csv

ec2 = boto3.client("ec2")

def get_ami_snapshot_associations():
    # Get all AMIs owned by the user
    response = ec2.describe_images(Owners=["self"])
    ami_data = {}

    for image in response["Images"]:
        ami_id = image["ImageId"]
        snapshot_ids = []

        # Loop through block device mappings to find associated snapshot IDs
        for mapping in image.get("BlockDeviceMappings", []):
            if "Ebs" in mapping and "SnapshotId" in mapping["Ebs"]:
                snapshot_ids.append(mapping["Ebs"]["SnapshotId"])

        # Store AMI ID and associated snapshots in dictionary
        ami_data[ami_id] = snapshot_ids

    return ami_data

def get_existing_snapshot_ids():
    # Get all snapshots owned by the user
    response = ec2.describe_snapshots(OwnerIds=["self"])
    return [snapshot["SnapshotId"] for snapshot in response["Snapshots"]]

def main():
    # Get AMIs and their associated snapshots
    ami_data = get_ami_snapshot_associations()
    # Get a list of all existing snapshot IDs
    existing_snapshot_ids = get_existing_snapshot_ids()

    # Open CSV file to write results
    with open("amis_without_snapshots.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["AMI ID", "AMI Name", "State", "Creation Date"])

        # Loop through AMIs and check for snapshots
        for ami_id, snapshot_ids in ami_data.items():
            # If no associated snapshots exist or they have been deleted
            if not snapshot_ids or all(snap_id not in existing_snapshot_ids for snap_id in snapshot_ids):
                # Get details about the AMI
                response = ec2.describe_images(ImageIds=[ami_id])
                ami_info = response["Images"][0]
                ami_name = ami_info.get("Name", "No Name")
                creation_date = ami_info["CreationDate"]
                state = ami_info["State"]

                # Write the AMI data to the CSV file
                writer.writerow([ami_id, ami_name, state, creation_date])

if __name__ == "__main__":
    main()

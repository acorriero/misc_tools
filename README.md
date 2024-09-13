# misc_tools

Miscellaneous tools used by IT Infrastructure department.

## ip_filter
Used to parse an nmap scan of a network and create a CSV file of the results.

## drs_rep_check
Check AWS DRS default replication settings and list any that are not default.

## ami_snapshots
A script that looks for snapshots created for an ami (using the description), then lookup if the ami still exists. If not, then those snapshots are good candidates to delete.

## unused_sg
Find unused security groups in AWS.

## ri_details
Get details about account's reserved instances.

## access_key_info
Get details about user's access keys.

## ami_missing_snapshots
A script that checks for AMIs that no longer have any snapshots associated with them.

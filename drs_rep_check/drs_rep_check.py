#!/usr/bin/env python3

import boto3


def get_source_hostnames(region):
    result = {}
    client = boto3.client('drs', region_name=region)

    response = client.describe_source_servers(
        filters={
            'stagingAccountIDs': []
        }
    )

    for i in response['items']:
        source_hostname = i['sourceProperties']['identificationHints']['hostname']
        source_id = i['sourceServerID']
        result[source_id] = source_hostname
    
    return result


def get_replication_configs(region):
    result = {}
    client = boto3.client('drs', region_name=region)

    source_ids = client.describe_source_servers(
        filters={
            'sourceServerIDs': []
        }
    )

    for i in source_ids['items']:
        rep_config = client.get_replication_configuration(
            sourceServerID = i['sourceServerID']
        )

        source_server_id = i['sourceServerID']
        disk_type = rep_config['defaultLargeStagingDiskType']
        inst_type = rep_config['replicationServerInstanceType']
        dedicated = rep_config['useDedicatedReplicationServer']

        result[source_server_id] = {'disk_type': disk_type,
                                    'inst_type': inst_type,
                                    'dedicated': dedicated}

    return result


def filter_sources(data):
    filtered_sources = {}
    for source_id, source_data in data.items():
        disk_type = source_data.get('disk_type', '')
        inst_type = source_data.get('inst_type', '')
        dedicated = source_data.get('dedicated', False)

        if disk_type != 'GP3' or inst_type != 't3.small' or dedicated != False:
            filtered_sources[source_id] = source_data
    
    return filtered_sources
        

def main():
    region = 'us-west-2'
    completed_list = {}
    source_servers = get_replication_configs(region)
    non_default_configs = filter_sources(source_servers)
    # Add Hostnames to the dictionary of source_ids
    source_hostnames = get_source_hostnames(region)
    for i in source_hostnames:
        if i in non_default_configs:
            completed_list[i] = {
                'HostName': source_hostnames[i],
                'DiskType': non_default_configs[i]['disk_type'],
                'InstanceType': non_default_configs[i]['inst_type'],
                'IsDedicated': non_default_configs[i]['dedicated']
            }
    
    for i in completed_list:
        print(i, completed_list[i])


if __name__ == "__main__":
    main()

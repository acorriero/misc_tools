#!/usr/bin/env python3

import re

def import_file(filename):
    with open(filename) as file:
        df = file.readlines()
    
    return df


def format_imported(file):
    formatted = {}
    hostname = ""
    ip_addr = ""
    mac_addr = ""
    additional_info = ""
    
    for line in file:
        if "Nmap scan report for" in line:
            parts = line.split("for ")
            if "(" not in parts[1]:
                hostname = "N/A"
                ip_addr = parts[1].strip()            
                formatted[ip_addr] = {'hostname': hostname}
            else:
                host_data = parts[1].split(" (")
                hostname = host_data[0].replace("${{env.domain}}", "")
                ip_addr = host_data[1].rstrip(")\n")
                formatted[ip_addr] = {'hostname': hostname}
        elif "MAC Address:" in line:
            mac_info = re.search(r"MAC Address:\s+([^\s]+)\s+\((.*?)\)", line)
            mac_addr = mac_info.group(1)
            additional_info = mac_info.group(2)
            formatted[ip_addr]['mac_addr'] = mac_addr
            formatted[ip_addr]['additional_info'] = additional_info

    return formatted


def create_csv(formatted):
    with open('ip-scan.csv', 'w') as file:
        file.write(f"IP, Hostname, MAC Address, Additional Info\n")
        for ip_addr, data in formatted.items():
            hostname = data['hostname']
            mac_addr = data.get('mac_addr', 'N/A')
            additional_info = data.get('additional_info', 'N/A')
            file.write(f"{ip_addr},{hostname},{mac_addr},{additional_info}\n")


def main():
    imported = import_file('hq-ip-scan.txt')
    formatted = format_imported(imported)
    create_csv(formatted)


if __name__ == "__main__":
    main()

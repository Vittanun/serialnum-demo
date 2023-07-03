from ipaddress import ip_network 

def host_ip (subnet):
    ips = list(ip_network(subnet))
    ip_hosts = []

    for ip in ips:
        ip_hosts.append(str(ip))

    return ip_hosts

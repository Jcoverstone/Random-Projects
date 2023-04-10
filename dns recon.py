import dns.resolver

# Set the DNS server to be used for queries
dns_server = '8.8.8.8'

# Set the domain to be queried
domain = 'example.com'

# Get the IP address of the DNS server
dns_ip = dns.resolver.query(dns_server, 'A')[0].address

# Get the IP addresses of the domain's name servers
ns_ips = [str(ip) for ip in dns.resolver.query(domain, 'NS')]

# Print the results
print(f"DNS server IP address: {dns_ip}")
print(f"Name server IP addresses: {', '.join(ns_ips)}")

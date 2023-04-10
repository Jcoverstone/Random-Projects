import dns.resolver

def resolve_domain(domain):
    """
    Resolves the A record for a given domain using Google DNS (8.8.8.8).

    Args:
        domain (str): The domain to resolve.

    Returns:
        str: The IP address of the A record.
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["8.8.8.8"]
    answer = resolver.query(domain, 'A')
    return answer[0].address

def print_a_records(domain):
    """
    Prints all A records for a given domain.

    Args:
        domain (str): The domain to query.
    """
    try:
        a_records = dns.resolver.query(domain, 'A')
        for record in a_records:
            print(f"Found A record for {domain}: {record.address}")
    except dns.resolver.NoAnswer:
        print(f"No A records found for {domain}")

if __name__ == '__main__':
    domain = 'example.com'
    ip_address = resolve_domain(domain)
    print(f"IP address of {domain}: {ip_address}")
    print_a_records(domain)
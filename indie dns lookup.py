import dns.resolver

def lookup_dns(domain, record_type="A"):
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 1.0
        resolver.lifetime = 1.0
        
        # Resolve the specified DNS record for the domain
        result = resolver.resolve(domain, record_type)

        # Extract the value of the resolved DNS record
        if record_type == "A":
            value = result[0].to_text()
        elif record_type == "MX":
            value = f"{result[0].exchange} (priority {result[0].preference})"
        elif record_type == "TXT":
            value = result[0].strings[0].decode("utf-8")
        else:
            value = result[0].to_text()

        return value
    except dns.exception.DNSException as e:
        print(f"DNS lookup failed for {domain}: {e}")
        return None
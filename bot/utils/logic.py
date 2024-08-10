def editor(domains):
    domains = domains.replace('{', '')
    domains = domains.replace('}', '')
    domains = domains.replace('\'', '')
    domains = domains.replace(',', '')

    return domains

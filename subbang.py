import subprocess
import re
import sys
import argparse

def print_usage():
    print("Usage:")
    print("python script_name.py -f domains_filename scope_filename")
    print("Example: python script_name.py -f domains.txt scope.txt")
    sys.exit(0)

def print_subbang():
    print(r"""
    SSSS   U   U  BBBB      BBBB   AAAAA  N   N  GGGGG
    S      U   U  B   B     B   B  A   A  NN  N  G   G
    SSSS   U   U  BBBB      BBBB   AAAAA  N N N  GGGGG  
       S   U   B  B   B     B   A  A   N  N  GG      G
    SSSS    UUU   BBBB      BBBB   A   A  N   N  GGGGG 
    """)


parser = argparse.ArgumentParser(description='Find subdomains in scope.')
parser.add_argument('-f', '--file', type=str, help='File containing domain names')
parser.add_argument('scope_file', type=str, help='File containing scope IPs')

args = parser.parse_args()

# Check for help flag
if '-h' in sys.argv or '--help' in sys.argv:
    print_usage()

# Function to execute the Bash command and capture subdomains
def get_subdomains_from_bash_command(domain):
    try:
        bash_command = f"curl -s https://crt.sh/\?q\={domain}\&output\=json | jq . | grep name | cut -d \":\" -f2 | grep -v \"CN=\" | cut -d '\"' -f2 | awk '{{gsub(/\\\\n/,\"\\n\");}}1;' | sort -u | grep -v C="
        result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
        subdomains = result.stdout.split('\n')
        return subdomains
    except Exception as e:
        print(f"Error occurred while executing the Bash command: {e}")
        return []

# If no file argument is provided, check if a single domain name is entered manually
if not args.file:
    print_subbang()
    domain_name = input("Enter your domain name: ")
    domains = [domain_name]
else:
    print_subbang()
    with open(args.file, 'r') as domains_file:
        domains = domains_file.readlines()

# Collect subdomains using the Bash command
collected_subdomains = []
for domain in domains:
    subdomains = get_subdomains_from_bash_command(domain.strip())
    collected_subdomains.extend(subdomains)

# Write collected subdomains to subdomains.txt
with open('subdomains.txt', 'w') as subdomains_output_file:
    subdomains_output_file.write('\n'.join(collected_subdomains))

# Function to map subdomains to IP addresses
def map_subdomains_to_ip(subdomains):
    ip_mapping = {}
    for subdomain in subdomains:
        try:
            # Run nslookup command
            result = subprocess.run(['nslookup', subdomain.strip()], capture_output=True, text=True, timeout=10)
            
            # Extract IP address using regex
            ip_addresses = re.findall(r'Address: ([\d.:a-fA-F]+)', result.stdout)
            
            # Filter out localhost and non-authoritative answers
            filtered_ips = [ip for ip in ip_addresses if ip != '127.0.0.53']
            
            if filtered_ips:
                ip_mapping[subdomain.strip()] = filtered_ips[0]  # Take the first IP address found
        except subprocess.TimeoutExpired:
            print(f"Timeout occurred while looking up {subdomain}. Skipping.")
        except Exception as e:
            print(f"Error occurred while looking up {subdomain}: {e}")
    
    return ip_mapping

# Read subdomains from subdomains.txt
with open('subdomains.txt', 'r') as subdomains_file:
    subdomains_list = subdomains_file.readlines()

# Call the function to map subdomains to IP addresses
ip_mapping_result = map_subdomains_to_ip(subdomains_list)

# Function to compare results with scope IPs and generate results.txt
def compare_results_with_scope(ip_mapping, scope_file):
    # Read IP addresses from scope.txt
    with open(scope_file, 'r') as scope_file:
        scope_ips = {line.strip() for line in scope_file}

    # Find matching IPs from nslookup results and scope.txt
    matching_pairs = {(subdomain, ip) for subdomain, ip in ip_mapping.items() if ip in scope_ips}

    # Print matching pairs and count the number of matches
    num_matches = len(matching_pairs)
    print(f"Found {num_matches} subdomains in scope!")

    # Write matching pairs to results.txt
    with open('results.txt', 'w') as results_file:
        results_file.write(f"Found {num_matches} subdomains in scope!\n")
        for subdomain, ip in matching_pairs:
            results_file.write(f"Hostname: {subdomain} IP: {ip}\n")
            print(f"Hostname: {subdomain} IP: {ip}")

# Call the function to compare results with scope.txt and generate results.txt
compare_results_with_scope(ip_mapping_result, args.scope_file)

# Mention the files where subdomains and in-scope results are written
print("All discovered subdomains written to subdomains.txt")
print("In scope results written to results.txt")

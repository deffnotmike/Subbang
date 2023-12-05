# About:
Subbang is a tool built to automate subdomain enumeration during a penetration test through the use of the CRT.SH website. Thank you ChatGPT for helping me iron out some of these functions.

# Usage:
Provide a single domain via the CLI or multiple domains through a file using the -f flag (--file) when running the tool.
Additionally, the scope.txt file is used to specify the IP addresses defining the scope of interest.

**Example 1:** Discover Subdomains for a Single Domain
\- Suppose the domain of interest is example.com:

Command:

```
python3 subbang.py scope.txt

Enter the domain name: example.com
```

This command will initiate the tool to retrieve subdomains associated with example.com, map them to their corresponding IP addresses, compare them against the IPs in scope.txt, and display the matching subdomains within the specified scope.

**Example 2:** Provide Multiple Domains via File
\- Suppose there is a file named domains.txt containing multiple domains:

Command:

```python3 subbang.py -f domains.txt scope.txt```

This command will run the tool for each domain listed in the domains.txt file. It will retrieve subdomains, map them to their corresponding IP addresses, and compare them against the IPs defined in scope.txt.

**Example 3:** Help Command
\- To get an explanation of how to use the tool:

Command:

```python3 subbang.py -h```

This command will display the tool's usage guide, showcasing each available option.

# Output Guide:
* All discovered subdomains, including out of scope subdomains, are written to subdomains.txt.
* Subdomains within the defined scope are written to results.txt.

# Conclusion:
This tool is specifically catered toward pentesters and bug bounty hunters who receive authorization from an organization to simulate an attacker attempting network/web-based intrusion.
**Educational purposes only.**

**Note:** There may be cases where load balancing affects scan results. Espcially when dealing with cloud-native hosts.

# TODOs:
* Allow users to specify an output location. Mergre output results into one file?...

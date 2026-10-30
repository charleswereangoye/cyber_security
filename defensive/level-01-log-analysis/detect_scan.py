#!/usr/bin/env python3
"""
Simple SOC Log Detection Script
Analyzes HTTP access logs to identify automated web scanning (e.g. Gobuster)
and potential unauthorized access attempts.
"""
import re
import sys
from collections import defaultdict

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3}) \S+ "(?P<referrer>[^"]*)" "(?P<agent>[^"]*)"'
)

def analyze_logs(logfile_path):
    print(f"[*] Analyzing log file: {logfile_path}...\n")
    ip_requests = defaultdict(int)
    scanner_hits = []
    status_summary = defaultdict(int)

    with open(logfile_path, "r") as f:
        for line in f:
            match = LOG_PATTERN.match(line.strip())
            if not match:
                continue
            
            data = match.groupdict()
            ip = data["ip"]
            agent = data["agent"]
            path = data["path"]
            status = data["status"]

            ip_requests[ip] += 1
            status_summary[status] += 1

            # Rule 1: Known scanner user-agents (Gobuster, sqlmap, nikto, dirbuster)
            if any(tool in agent.lower() for tool in ["gobuster", "sqlmap", "nikto", "dirbuster"]):
                scanner_hits.append((ip, agent, path, status))

    print("=== 1. TRAFFIC VOLUME BY IP ===")
    for ip, count in ip_requests.items():
        print(f"IP: {ip:<15} Requests: {count}")

    print("\n=== 2. HTTP STATUS CODE DISTRIBUTION ===")
    for code, count in sorted(status_summary.items()):
        print(f"HTTP {code}: {count} responses")

    print("\n=== 3. DETECTED THREATS / AUTOMATED SCANS ===")
    if scanner_hits:
        print(f"[!] ALERT: Found {len(scanner_hits)} requests originating from known automated scanners!")
        for ip, agent, path, status in scanner_hits[:5]:
            print(f"  - [{status}] {ip} requested '{path}' using User-Agent: '{agent}'")
        if len(scanner_hits) > 5:
            print(f"  ... and {len(scanner_hits) - 5} more probe events.")
    else:
        print("[+] No known automated scanner signatures detected.")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "sample-access.log"
    analyze_logs(path)

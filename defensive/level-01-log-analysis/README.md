# Defensive Lab 1: Web Scanner & Fuzzer Detection

## Metadata
- **Track**: Defensive Security
- **Difficulty**: Beginner
- **Category**: Security Operations Center (SOC), Log Analysis, Threat Detection

---

## Overview

Automated tools such as Gobuster, DirBuster, and ffuf generate distinct operational signatures in web server access logs (`access.log`):

1. **High Request Velocity**: Large volumes of HTTP requests submitted within narrow time windows.
2. **Elevated 404 Error Rates**: Unusually high ratios of `404 Not Found` responses relative to baseline traffic.
3. **Tool-Specific User-Agent Headers**: Default identification strings (e.g., `gobuster/<version>`).
4. **Targeting of Sensitive Paths**: Systematic probing for common administrative or configuration endpoints (`.env`, `.git`, `backup.zip`).

---

## Objectives

1. Analyze standard HTTP Combined Log Format records.
2. Identify automated scanning patterns using command-line triage tools.
3. Execute the provided Python log detection script to summarize threat activity.
4. Review standard hardening techniques to block automated scanning.

---

## Practical Analysis

### Automated Detection Script
Execute `detect_scan.py` against the included log sample:
```bash
./detect_scan.py sample-access.log
```

### Manual CLI Triage
Standard Linux utilities provide fast triage for incident response:

1. **Count requests by source IP**:
   ```bash
   awk '{print $1}' sample-access.log | sort | uniq -c | sort -nr
   ```

2. **Filter requests by Gobuster User-Agent**:
   ```bash
   grep -i "gobuster" sample-access.log
   ```

3. **Identify endpoints that responded successfully (`HTTP 200`) during the scan**:
   ```bash
   grep " 200 " sample-access.log | grep -i "gobuster"
   ```

---

## Remediation and Hardening

1. **Rate Limiting**: Enforce request rate thresholds (e.g., via Nginx `limit_req_zone` or WAF policies) to drop traffic exceeding standard browsing speeds.
2. **Automated IP Blocking**: Integrate tools such as Fail2ban to monitor log events and dynamically ban IPs that generate sustained 404 response bursts.
3. **Extension Restrictions**: Configure web servers to explicitly deny access to sensitive backup extensions:
   ```nginx
   # Nginx: Block direct access to backup files and sensitive extensions
   location ~* \.(bak|config|sql|old|env|git|txt)$ {
       deny all;
       return 404;
   }
   ```

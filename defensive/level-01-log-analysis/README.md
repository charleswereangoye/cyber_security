# Defensive Lab 1: Detecting Automated Fuzzers & Web Scanners

## Overview
- **Track**: Defensive Security (Blue Team)
- **Difficulty**: Easy
- **Category**: Security Operations Center (SOC), Log Analysis, Threat Detection
- **Estimated Time**: 20 minutes

---

## Background & Theory

Offensive tools like Gobuster, DirBuster, and ffuf are fast, but they are also **loud**. Unless an attacker manually changes their User-Agent or throttles their rate of requests, their activity leaves unmistakable fingerprints in web server logs (`access.log`):

1. **High Request Velocity**: Hundreds of requests per second from a single IP address.
2. **Abnormal 404 Spikes**: High ratio of `404 Not Found` responses compared to `200 OK`.
3. **Default User-Agent Signatures**: Gobuster sends `User-Agent: gobuster/<version>` unless told otherwise (`-a` flag).
4. **Targeted Sensitive Endpoints**: Probing for common paths (`.env`, `.git`, `wp-admin`, `backup.zip`).

---

## Lab Objectives

1. Understand standard HTTP access log formats.
2. Inspect `sample-access.log` to identify attacker behavior.
3. Use command-line tools (`grep`, `awk`, `sort`) and the included Python detection script to detect brute-force activity.
4. Learn defensive hardening rules to mitigate this attack.

---

## Hands-On Exercise

### Step 1: Run the Detection Script
Run the automated detection script against the sample log:
```bash
./detect_scan.py sample-access.log
```

### Step 2: Manual Log Analysis with Linux Commands
Real SOC analysts often use Linux utilities for quick triage:

1. **Identify the top requesting IP addresses**:
   ```bash
   awk '{print $1}' sample-access.log | sort | uniq -c | sort -nr
   ```
2. **Find all requests made by Gobuster**:
   ```bash
   grep -i "gobuster" sample-access.log
   ```
3. **Check which sensitive files were successfully accessed (HTTP 200)**:
   ```bash
   grep " 200 " sample-access.log | grep -i "gobuster"
   ```

---

## Blue Team Defensive Recommendations

How do we stop attackers from exploiting these vulnerabilities in production?

1. **Web Application Firewall (WAF) / Rate Limiting**:
   Use Nginx rate limiting or Cloudflare WAF to drop requests exceeding reasonable user thresholds (e.g., limit to 10 requests/second per IP).
2. **Fail2ban Integration**:
   Configure Fail2ban to parse access logs and automatically add temporary firewall (`iptables` / `nftables`) bans for IPs generating excessive 404 errors.
3. **Server Configuration Hardening**:
   Block direct access to sensitive extensions at the web server level (Nginx/Apache):
   ```nginx
   # Nginx example: Deny access to hidden files and backup extensions
   location ~* \.(bak|config|sql|old|env|git|txt)$ {
       deny all;
       return 404;
   }
   ```

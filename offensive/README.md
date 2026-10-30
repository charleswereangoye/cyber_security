# Offensive Security Track (Red Team)

Welcome to the **Offensive Security Practice Track**. This track teaches practical web application penetration testing, reconnaissance, vulnerability discovery, and exploitation techniques using hands-on CTF-style challenges.

---

## Prerequisites & Tools

Before running these labs, ensure you have the following installed on your machine:

1. **Podman** (Rootless container engine):
   ```bash
   podman --version
   ```
2. **Gobuster** (High-speed directory and file brute-forcing tool):
   ```bash
   gobuster version
   ```
3. **Wordlists**:
   Standard wordlists (e.g., `common.txt` or `directory-list-2.3-medium.txt` from SecLists).

---

## Offensive Methodology

Each level follows the standard penetration testing lifecycle:

```
┌─────────────────────────────────┐
│ 1. Passive & Active Recon       │ (Inspect robots.txt, headers, source)
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│ 2. Enumeration & Fuzzing        │ (Gobuster directory & extension scans)
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│ 3. Vulnerability Analysis       │ (Analyze leaks, 403 endpoints, parameters)
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│ 4. Exploitation & Flags         │ (Auth bypass, extract sensitive data)
└─────────────────────────────────┘
```

---

## Lab Curriculum

| Level | Topic | Key Skills | Difficulty |
| :--- | :--- | :--- | :--- |
| **[Level 1](level-01-recon-robots/)** | Robots.txt & Basic Recon | `robots.txt` information disclosure, default Gobuster scans | 🟢 Very Easy |
| **[Level 2](level-02-extension-fuzzing/)** | Extension Fuzzing & Leaks | Gobuster `-x` flag (`.bak`, `.txt`), HTTP 403 analysis, auth bypass | 🟡 Easy |
| **Level 3** | Parameter Fuzzing & Injection | Coming soon | 🟠 Intermediate |

---

## Quick Lab Commands

From the repository root:
* Start Level 1: `./start-lab.sh 1`
* Start Level 2: `./start-lab.sh 2`
* Stop target: `./stop-lab.sh`

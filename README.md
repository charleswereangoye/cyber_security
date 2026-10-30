# Cybersecurity Hands-On Training Lab 🛡️⚔️

An interactive, containerized learning environment designed to take beginners from zero to hands-on proficiency in both **Offensive Hacking (Red Team)** and **Defensive Security (Blue Team)**.

All practice targets are isolated and run locally using **Podman** (no cloud machines or outdated physical devices required).

---

## 📁 Repository Architecture

```text
cyber_security/
├── offensive/                       # Red Team Track (Penetration Testing & Exploitation)
│   ├── README.md                    # Methodology, tools, and offensive curriculum
│   ├── level-01-recon-robots/       # Level 1: robots.txt Recon & Directory Brute-Forcing
│   │   ├── Containerfile
│   │   ├── server.py
│   │   ├── robots.txt
│   │   ├── admin/index.html
│   │   └── README.md
│   └── level-02-extension-fuzzing/  # Level 2: Extension Fuzzing & Sensitive File Leaks
│       ├── Containerfile
│       ├── server.py
│       └── README.md
│
├── defensive/                       # Blue Team Track (Detection, Logging & Hardening)
│   ├── README.md                    # Blue team principles & threat hunting
│   └── level-01-log-analysis/       # Lab 1: Detecting Automated Scanners in Web Logs
│       ├── sample-access.log
│       ├── detect_scan.py
│       └── README.md
│
├── start-lab.sh                     # Unified lab runner script
├── stop-lab.sh                      # Universal target stop script
└── README.md                        # Master curriculum guide (this file)
```

---

## 🚀 Prerequisites

Before starting, make sure you have the following tools installed on your Linux machine:

1. **Podman** (Rootless container engine):
   ```bash
   podman --version
   ```
2. **Gobuster** (Directory & file brute-forcing CLI):
   ```bash
   gobuster version
   ```
3. **Wordlist**:
   A standard wordlist (such as `/home/chaleeblack/common.txt` or SecLists `directory-list-2.3-medium.txt`).

---

## ⚡ Quickstart: Launching Practice Targets

Use the master runner script [start-lab.sh](file:///home/chaleeblack/cyber_security/start-lab.sh) to spin up any lab:

### Launch Level 1 (Offensive)
```bash
./start-lab.sh 1
```
*Target URL: `http://127.0.0.1:8080`*

### Launch Level 2 (Offensive)
```bash
./start-lab.sh 2
```
*Target URL: `http://127.0.0.1:8080`*

### Stop Any Active Target
```bash
./stop-lab.sh
```

---

## 🎯 Curriculum Tracks

### ⚔️ 1. Offensive Security Track (Red Team)
*Detailed guide: [offensive/README.md](file:///home/chaleeblack/cyber_security/offensive/README.md)*

| Level | Focus | Key Concepts & Tools | Status |
| :--- | :--- | :--- | :--- |
| **[Level 1](offensive/level-01-recon-robots/)** | Robots.txt & Basic Recon | Passive reconnaissance, `robots.txt` information disclosure, default Gobuster scans | ✅ Complete |
| **[Level 2](offensive/level-02-extension-fuzzing/)** | Extension Fuzzing & Leaks | Gobuster `-x` flag (`.bak`, `.txt`, `.json`), HTTP `403 Forbidden` analysis, token authentication bypass | ✅ Complete |
| **Level 3** | Parameter Fuzzing & Injection | Hidden parameter discovery (`ffuf`/`wfuzz`), command injection | 🚧 Coming Next |

### 🛡️ 2. Defensive Security Track (Blue Team)
*Detailed guide: [defensive/README.md](file:///home/chaleeblack/cyber_security/defensive/README.md)*

| Lab | Focus | Key Concepts & Tools | Status |
| :--- | :--- | :--- | :--- |
| **[Lab 1](defensive/level-01-log-analysis/)** | Web Scanner Detection | Inspecting HTTP access logs, identifying Gobuster signatures, high-velocity request spikes, writing automated Python log detectors | ✅ Complete |

---

## 📖 Recommended Workflow for Junior Learners

1. **Start with the Target**: Launch a level using `./start-lab.sh <level>`.
2. **Never Look at the Solution First**: Try reading the scenario in each level's `README.md` and attacking it blind.
3. **Inspect HTTP Responses**: Use `curl -I` and your browser's Developer Tools (Network tab) to understand HTTP response codes (`200`, `301`, `403`, `404`).
4. **Pivot to Defense**: Once you breach a level in the offensive track, study the corresponding defensive lab to learn how defenders detect and block the exact technique you just used.
5. **Always Clean Up**: Run `./stop-lab.sh` when you're finished.

---

## ⚖️ Legal & Ethical Disclaimer

All tools and scripts in this repository are strictly intended for educational, authorized training in isolated local environments. Never scan or test systems without explicit written permission.

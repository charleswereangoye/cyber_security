# Cyber Security Training Labs

A containerized hands-on security training laboratory featuring offensive and defensive exercises powered by Podman. This repository provides an isolated environment for learning web application security fundamentals, active reconnaissance, content discovery, and defensive log analysis.

---

## Architecture

```text
cyber_security/
├── offensive/                       # Offensive security exercises (Red Team)
│   ├── README.md                    # Methodology and module overview
│   ├── level-01-recon-robots/       # Information disclosure via robots.txt
│   └── level-02-extension-fuzzing/  # Sensitive file leakage and extension fuzzing
│
├── defensive/                       # Defensive security exercises (Blue Team)
│   ├── README.md                    # Defensive methodology and log monitoring
│   └── level-01-log-analysis/       # Automated web scanner detection in access logs
│
├── wordlists/                       # Bundled wordlists for local fuzzing
│   └── common.txt                   # Standard discovery wordlist
│
├── start-lab.sh                     # Lab launcher script
├── stop-lab.sh                      # Universal container stop script
└── README.md                        # Project documentation
```

---

## Prerequisites

The following tools are required to run and interact with the practice environments:

1. **Podman** (v4.0+ recommended)
   ```bash
   podman --version
   ```
2. **Gobuster** (v3.0+) or any standard HTTP directory enumeration tool
   ```bash
   gobuster version
   ```
3. **cURL** and a modern web browser

---

## Getting Started

### 1. Launch a Lab Target

Use `start-lab.sh` followed by the level number to build and run the corresponding target container:

- Launch Level 1:
  ```bash
  ./start-lab.sh 1
  ```

- Launch Level 2:
  ```bash
  ./start-lab.sh 2
  ```

Once started, the target server binds locally to port 8080: `http://127.0.0.1:8080`.

### 2. Stop the Active Target

To stop and remove the active lab container:
```bash
./stop-lab.sh
```

---

## Curriculum Overview

### Offensive Track (Red Team)

Detailed instructions and background theory are available in [offensive/README.md](offensive/README.md).

| Level | Focus | Key Topics | Difficulty |
| :--- | :--- | :--- | :--- |
| [Level 1](offensive/level-01-recon-robots/) | Reconnaissance & Discovery | `robots.txt` information disclosure, directory enumeration | Beginner |
| [Level 2](offensive/level-02-extension-fuzzing/) | Extension Fuzzing & Leaks | Gobuster `-x` flag, backup file leakage, auth bypass | Beginner |
| Level 3 | Parameter Fuzzing & Injection | Hidden parameter enumeration, input validation | Intermediate (Planned) |

### Defensive Track (Blue Team)

Detailed instructions and background theory are available in [defensive/README.md](defensive/README.md).

| Lab | Focus | Key Topics | Difficulty |
| :--- | :--- | :--- | :--- |
| [Lab 1](defensive/level-01-log-analysis/) | Scanner Detection | Web server log triage, User-Agent tracking, automated detection | Beginner |

---

## Recommended Workflow

1. Start the target container with `./start-lab.sh <level>`.
2. Review the scenario and objectives in the corresponding level's `README.md`.
3. Conduct discovery using Gobuster with the bundled wordlist:
   ```bash
   gobuster dir -u http://127.0.0.1:8080 -w wordlists/common.txt
   ```
4. Analyze findings and execute the objective.
5. Review the defensive counterpart to understand how the activity is logged and detected.
6. Stop the environment using `./stop-lab.sh`.

---

## Security and Legal Notice

All exercises in this repository are designed strictly for educational use in controlled local environments. Do not scan or target systems without explicit authorization.

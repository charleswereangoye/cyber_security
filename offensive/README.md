# Offensive Security Track

This track covers web application security testing, reconnaissance, content discovery, and vulnerability assessment.

---

## Environment Setup

Ensure the following tools are available:

1. **Podman**
2. **Gobuster**
3. **Wordlists**: A standard wordlist is bundled at `wordlists/common.txt`. Additional wordlists can be pulled from SecLists if desired.

---

## Methodology

Each exercise simulates a common phase of the penetration testing lifecycle:

1. **Reconnaissance**: Passive inspection of site structure, response headers, and metadata (`robots.txt`, comments).
2. **Enumeration**: Automated scanning using wordlists and targeted file extensions.
3. **Analysis**: Interpreting HTTP response codes (`200`, `301`, `403`, `404`) and reviewing discovered assets.
4. **Exploitation**: Leveraging findings to access protected functionality or extract sensitive data.

---

## Modules

| Module | Description | Objectives |
| :--- | :--- | :--- |
| [Level 1: Reconnaissance & Robots.txt](level-01-recon-robots/) | Information disclosure via `robots.txt` | Practice baseline directory enumeration and flag retrieval. |
| [Level 2: Extension Fuzzing & Backups](level-02-extension-fuzzing/) | Fuzzing file extensions for developer leaks | Identify unlinked backup files and bypass access restrictions. |
| Level 3: Parameter Fuzzing & Injection | Parameter discovery and command execution | In development. |

---

## Usage

Start any offensive lab from the repository root:

```bash
./start-lab.sh 1    # Start Level 1
./start-lab.sh 2    # Start Level 2
./stop-lab.sh       # Stop running target
```

# Defensive Security Track

This track focuses on threat detection, log analysis, security operations center (SOC) triage, and system hardening techniques.

---

## Core Focus Areas

1. **Log Analysis & Monitoring**: Identifying malicious or automated web patterns within server and access logs.
2. **Threat Detection**: Developing detection rules and automation scripts to spot brute-force attacks and vulnerability scanning.
3. **Remediation & Hardening**: Implementing principle of least privilege, rate limiting, and web server configuration controls.

---

## Modules

| Module | Description | Objectives |
| :--- | :--- | :--- |
| [Lab 1: Web Scanner Detection](level-01-log-analysis/) | Detection of Gobuster scans in access logs | Analyze request velocity, User-Agent signatures, and 404 response ratios. |

---

## Recommended Workflow

1. Perform the corresponding offensive exercise to observe the attack perspective.
2. Review the resulting web server logs or provided sample logs.
3. Develop and execute detection scripts or queries to isolate attacker traffic.
4. Apply the recommended server hardening measures.

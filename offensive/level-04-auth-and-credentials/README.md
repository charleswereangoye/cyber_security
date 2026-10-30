# Level 4: Authentication Flaws & Credential Auditing

## Metadata
- **Track**: Offensive Security
- **Difficulty**: Beginner
- **Category**: Identification and Authentication Failures (OWASP Top 10 - A07:2021)
- **Concepts**: HTTP POST Requests, Username Enumeration, Verbose Error Responses, Default Credentials

---

## Overview

Authentication mechanisms are among the most frequently attacked components of any web application. Developers commonly introduce two subtle but serious vulnerabilities when building login systems:

1. **Username Enumeration via Verbose Errors**: 
   When an authentication endpoint differentiates between an invalid username (*"Account does not exist"*) and an invalid password (*"Incorrect password for user X"*), an attacker can easily verify which accounts exist on the system.

2. **Default or Weak Credentials**:
   Applications, administrative panels, and newly provisioned employee accounts are frequently deployed with predictable temporary passwords (e.g., `admin`, `password`, `welcome123`). If default credentials are not forcefully rotated on first login, attackers can immediately access privileged roles.

In this exercise, you will also transition from simple HTTP `GET` requests to handling HTTP `POST` requests, which transmit credentials in the HTTP request body.

---

## Objectives

1. Deploy the Level 4 target container using Podman.
2. Access the Staff Authentication portal at `http://127.0.0.1:8080/login`.
3. Submit login requests to analyze how the application handles invalid usernames versus valid usernames.
4. Confirm user enumeration, identify the administrative username, and test common default credentials.
5. Authenticate to the staff dashboard and capture the flag.

---

## Deployment

From the repository root:
```bash
./start-lab.sh 4
```

Confirm service availability:
```bash
curl -I http://127.0.0.1:8080/login
```

---

## Walkthrough

### Step 1: Analyze Error Behavior (User Enumeration)
Submit a login request with an arbitrary, fake username:
```bash
curl -s -X POST -d "username=nonexistent_user&password=test" http://127.0.0.1:8080/login | grep "alert"
```
*Response: Notice the server explicitly reports that the username does not exist.*

Now test with a standard administrative account name (`admin`):
```bash
curl -s -X POST -d "username=admin&password=wrongpassword" http://127.0.0.1:8080/login | grep "alert"
```
*Response: The server reports `Incorrect password supplied for account 'admin'`. This confirms that the user `admin` exists on the system!*

### Step 2: Test Default Credentials
Once a valid username is confirmed, test common administrative default passwords:
- `admin`
- `password`
- `123456`
- `welcome`

Submit the login with `username=admin` and `password=password`:

**Via Browser:**
Navigate to `http://127.0.0.1:8080/login`, enter `admin` and `password`, and click **Authenticate**.

**Via Command Line:**
```bash
curl -s -X POST -d "username=admin&password=password" http://127.0.0.1:8080/login | grep -i "Flag{"
```

The portal grants authenticated access to the Staff Dashboard and displays **Flag 4**!

---

## Full-Stack Developer Remediation

### 1. Prevent Username Enumeration
Always return generic, consistent error messages regardless of whether the username exists or the password was incorrect:

```python
# INSECURE (Leans information):
if not user:
    return "User account does not exist."
if not verify_password(password, user.hash):
    return "Incorrect password for user."

# SECURE (Consistent response):
if not user or not verify_password(password, user.hash):
    return "Invalid username or password."
```

### 2. Force Credential Rotation
Never permit users to operate with default passwords. Implement a `must_change_password` flag in the database that redirects new users to a password reset flow immediately upon their first login.

### 3. Implement Rate Limiting and Account Lockouts
Prevent automated brute-force attacks by rate-limiting login attempts (e.g., maximum 5 attempts per IP or account per minute) using Redis or middleware like `express-rate-limit`.

---

## Teardown
```bash
./stop-lab.sh
```

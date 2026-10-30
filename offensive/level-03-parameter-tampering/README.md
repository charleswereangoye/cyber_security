# Level 3: Parameter Tampering & Insecure Direct Object References (IDOR)

## Metadata
- **Track**: Offensive Security
- **Difficulty**: Beginner
- **Category**: Broken Access Control (OWASP Top 10 - A01:2021)
- **Concepts**: URL Parameter Tampering, Authorization Bypasses, Insecure Direct Object References (IDOR)

---

## Overview

In modern web development, applications regularly reference database records directly via URL query parameters or route parameters:

```text
https://example.com/recipe?id=1
https://example.com/api/orders/1042
https://example.com/profile?user_id=88
```

An **Insecure Direct Object Reference (IDOR)** occurs when an application uses client-provided input to access an object directly in the backend without verifying whether the requesting user has the authorization to view or modify that object.

Developers often assume that because a confidential link is not rendered on the public menu or homepage, users will never find it. However, because database IDs are sequential or predictable integers (`1`, `2`, `3`...), an attacker can simply increment or change the identifier to view sensitive data.

---

## Objectives

1. Deploy the Level 3 target container using Podman.
2. Inspect the public recipe catalog at `http://127.0.0.1:8080/`.
3. Observe how the application handles requests for specific recipes using the `?id=` query parameter.
4. Tamper with the `id` parameter to locate unlisted, confidential recipes and retrieve the flag.

---

## Deployment

From the repository root:
```bash
./start-lab.sh 3
```

Confirm service availability:
```bash
curl -I http://127.0.0.1:8080/
```

---

## Walkthrough

### Step 1: Baseline Analysis
Open `http://127.0.0.1:8080/` in your browser or request the homepage via `curl`:
```bash
curl -s http://127.0.0.1:8080/
```

Notice that two public recipes are listed:
- **Recipe #1**: `/recipe?id=1` (Classic French Omelette)
- **Recipe #2**: `/recipe?id=2` (Tuscan Garlic Pasta)

### Step 2: Observe the Parameter Pattern
Retrieve Recipe #1:
```bash
curl -s "http://127.0.0.1:8080/recipe?id=1"
```
The application loads the recipe using the `id=1` parameter.

### Step 3: Parameter Tampering (IDOR)
Because database keys are typically sequential integers, test adjacent numbers:
```bash
curl -s "http://127.0.0.1:8080/recipe?id=3"
```

The server responds with `HTTP 200` and displays the **Executive Chef Confidential: Grand Reserve Truffle Glaze**, exposing the restricted flag!

---

## Full-Stack Developer Remediation

Why did this vulnerability exist in the code?

### Vulnerable Backend Pattern (Anti-Pattern)
```python
# The server fetches whatever ID the user sends without verifying permissions:
recipe_id = request.args.get("id")
recipe = db.get(recipe_id)

return render_template("recipe.html", recipe=recipe)
```

### Secure Backend Pattern
In production applications, access control checks must be enforced on the server for every single object request:

```python
recipe_id = request.args.get("id")
recipe = db.get(recipe_id)

if not recipe:
    abort(404)

# Enforce authorization check:
if recipe.is_secret and not current_user.has_role("executive_chef"):
    abort(403)  # Access Denied: User is not authorized to view this record

return render_template("recipe.html", recipe=recipe)
```

---

## Teardown
```bash
./stop-lab.sh
```

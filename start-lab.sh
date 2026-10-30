#!/usr/bin/env bash
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEVEL="${1:-2}"

if [ "$LEVEL" == "1" ]; then
    TARGET_DIR="$REPO_ROOT/offensive/level-01-recon-robots"
    IMAGE_NAME="offensive-level-1"
    echo "[*] Selected Level 1: Reconnaissance & Robots.txt"
elif [ "$LEVEL" == "2" ]; then
    TARGET_DIR="$REPO_ROOT/offensive/level-02-extension-fuzzing"
    IMAGE_NAME="offensive-level-2"
    echo "[*] Selected Level 2: Extension Fuzzing & Leaked Backups"
else
    echo "Usage: $0 [1|2]"
    echo "  1 - Start Level 1 (Robots.txt & Basic Recon)"
    echo "  2 - Start Level 2 (Extension Fuzzing & Leaked Backups)"
    exit 1
fi

# Stop and remove existing lab container if running
if podman ps -a --filter "name=offensive-lab" --format "{{.Names}}" | grep -q "^offensive-lab$"; then
    echo "[*] Stopping existing offensive-lab container..."
    podman stop offensive-lab >/dev/null 2>&1 || true
    podman rm offensive-lab >/dev/null 2>&1 || true
fi

# Build image
echo "[*] Building $IMAGE_NAME image with Podman..."
podman build -t "$IMAGE_NAME" "$TARGET_DIR"

# Run container
echo "[*] Launching offensive-lab container on port 8080..."
podman run -d --name offensive-lab -p 8080:8080 "localhost/$IMAGE_NAME"
sleep 1

echo ""
echo "=================================================="
echo "[+] SUCCESS: Lab Level $LEVEL is live!"
echo "[+] Target Address: http://127.0.0.1:8080"
echo "=================================================="
echo "To test the endpoint: curl -I http://127.0.0.1:8080/"
echo "To stop this lab:     ./stop-lab.sh"

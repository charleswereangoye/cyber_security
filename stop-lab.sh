#!/usr/bin/env bash
echo "[*] Stopping offensive-lab container..."
if podman ps -a --filter "name=offensive-lab" --format "{{.Names}}" | grep -q "^offensive-lab$"; then
    podman stop offensive-lab >/dev/null 2>&1 || true
    podman rm offensive-lab >/dev/null 2>&1 || true
    echo "[+] Container offensive-lab stopped and removed cleanly."
else
    echo "[-] No offensive-lab container is currently running."
fi

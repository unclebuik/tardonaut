#!/usr/bin/env bash
set -euo pipefail

# Tardonaut (TDNT)
# Read-only authority verification.

MINT="FGzxGmzsEsYV7D9RoFCQqrJ8fMcyEspcbgT7B1niTmsM"

echo "TARDONAUT — AUTHORITY VERIFICATION"

RPC=$(solana config get |
    awk '/^RPC URL:/ {print $3}' |
    tr -d '\r')

if [[ "$RPC" != "https://api.devnet.solana.com" ]]; then
    echo "ERROR: Devnet required."
    exit 1
fi

INFO=$(spl-token --program-2022 display "$MINT")

echo "$INFO"

if ! grep -Eq \
    '^[[:space:]]*Mint authority:[[:space:]]*\(not set\)$' \
    <<< "$INFO"; then
    echo "ERROR: Mint authority is active."
    exit 1
fi

if ! grep -Eq \
    '^[[:space:]]*Freeze authority:[[:space:]]*\(not set\)$' \
    <<< "$INFO"; then
    echo "ERROR: Freeze authority is active."
    exit 1
fi

echo
echo "VERIFICATION SUCCESSFUL"
echo "Mint authority: Revoked"
echo "Freeze authority: Not set"
echo "Metadata authority: Unchanged"

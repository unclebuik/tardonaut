#!/bin/bash
set -euo pipefail

# Tardonaut (TDNT)
# Development network: Solana Devnet

echo "TARDONAUT — TOKEN CREATION"

# Require Devnet.
RPC=$(solana config get | grep "RPC URL:")

if [[ "$RPC" != *"https://api.devnet.solana.com"* ]]; then
    echo "ERROR: Solana Devnet is required."
    exit 1
fi

# Check wallet.
echo
echo "Wallet:"
solana address

echo
echo "Balance:"
solana balance

# Create Token-2022 mint with metadata extension.
echo
echo "Creating Tardonaut Token-2022 mint..."

spl-token --program-id \
    TokenzQdBNbLqP5VEhdkAS6EPFjGz3oTgkYy5v4qLq3 \
    create-token \
    --decimals 6 \
    --enable-metadata

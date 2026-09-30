#!/bin/bash

# Verify the Solana meme coin mint and token account.

set -e

CONFIG="config/token.json"

if [ ! -f "$CONFIG" ]; then
    echo "Missing $CONFIG"
    exit 1
fi

MINT_ADDRESS=$(grep '"mint_address"' "$CONFIG" | cut -d '"' -f 4)

if [ -z "$MINT_ADDRESS" ]; then
    echo "mint_address is empty in $CONFIG"
    exit 1
fi

echo "================================"
echo "SOLANA MEME COIN VERIFICATION"
echo "================================"

echo
echo "Network:"
solana config get

echo
echo "Wallet:"
solana address

echo
echo "Mint:"
echo "$MINT_ADDRESS"

echo
echo "Mint information:"
spl-token display "$MINT_ADDRESS"

echo
echo "Token balance:"
spl-token balance "$MINT_ADDRESS"

echo
echo "Token accounts:"
spl-token accounts "$MINT_ADDRESS"

echo
echo "Verification complete."

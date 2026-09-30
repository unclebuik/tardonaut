#!/bin/bash

# Mint the configured supply to the wallet that owns the token mint.

set -e

CONFIG="config/token.json"

if [ ! -f "$CONFIG" ]; then
    echo "Missing $CONFIG"
    exit 1
fi

MINT_ADDRESS=$(grep '"mint_address"' "$CONFIG" | cut -d '"' -f 4)
TOTAL_SUPPLY=$(grep '"total_supply"' "$CONFIG" | cut -d '"' -f 4)

if [ -z "$MINT_ADDRESS" ]; then
    echo "mint_address is empty in $CONFIG"
    exit 1
fi

if [ -z "$TOTAL_SUPPLY" ]; then
    echo "total_supply is empty in $CONFIG"
    exit 1
fi

echo "Token mint:"
echo "$MINT_ADDRESS"

echo
echo "Supply:"
echo "$TOTAL_SUPPLY"

echo
echo "Creating token account..."

spl-token create-account "$MINT_ADDRESS"

echo
echo "Minting tokens..."

spl-token mint "$MINT_ADDRESS" "$TOTAL_SUPPLY"

echo
echo "Token balance:"

spl-token balance "$MINT_ADDRESS"

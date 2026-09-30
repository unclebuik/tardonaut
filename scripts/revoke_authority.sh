#!/bin/bash

# Permanently disable mint and freeze authorities.
# This should only be used after the final token supply has been minted.

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

echo "Token mint:"
echo "$MINT_ADDRESS"

echo
echo "WARNING:"
echo "This operation permanently disables the authorities."
echo "Minting additional tokens will no longer be possible."
echo "Freezing token accounts will no longer be possible."

echo
read -r -p "Type REVOKE to continue: " CONFIRM

if [ "$CONFIRM" != "REVOKE" ]; then
    echo "Operation cancelled."
    exit 0
fi

echo
echo "Disabling mint authority..."

spl-token authorize "$MINT_ADDRESS" mint --disable

echo
echo "Disabling freeze authority..."

spl-token authorize "$MINT_ADDRESS" freeze --disable

echo
echo "Authorities revoked."

echo
echo "Final mint information:"

spl-token display "$MINT_ADDRESS"

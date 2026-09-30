# Meme Coin

A Solana meme coin project.

## Project

This project creates and manages a basic SPL token on Solana.

## Network

Development network:

- Solana Devnet

Production network:

- Solana Mainnet

The project must be tested completely on Devnet before Mainnet deployment.

## Token

- Name: Meme Coin
- Symbol: MEME
- Decimals: 6
- Total supply: 1,000,000,000
- Transfer tax: None
- Buy tax: None
- Sell tax: None

## Structure

```text
meme_coin/
├── config/
│   └── token.json
├── metadata/
│   └── token.json
├── scripts/
│   ├── create_token.sh
│   ├── mint_token.sh
│   ├── verify_token.sh
│   └── revoke_authority.sh
├── assets/
│   └── logo.png
├── README.md
└── .gitignore

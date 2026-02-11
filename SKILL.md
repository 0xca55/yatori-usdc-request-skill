# Yatori USDC Request Skill

Generate USDC payment request links for the [Yatori](https://yatori.io) mobile payment system.

## Installation

```bash
curl -sSL https://yatori.io/agents/yatori-usdc-request-skill/install.sh | bash
```

## Quick Start

```python
from skill import create_payment_link

# Generate a payment link
link = create_payment_link(
    recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
    amount=5.0  # $5.00 USDC
)

print(link)
# https://yatori.io/mobile/yatoriRequest?token=usdcBasic&to=...&amount=5.00&yid=abc123
```

## Features

- 💳 **Smart Token Detection** — Auto-detects `usdcBasic` vs `usdcCreate`
- 🔒 **Address Validation** — Validates Solana addresses
- 💰 **Amount Limits** — $0.01 minimum, $10,000.00 maximum
- 🆔 **Auto-Generated IDs** — Unique tracking IDs for each request

## API Reference

### `create_payment_link(recipient, amount, yid=None, token=None)`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `recipient` | str | ✅ | Solana wallet address (32-44 chars) |
| `amount` | float | ✅ | Amount in USDC ($0.01 - $10,000.00) |
| `yid` | str | ❌ | Unique transaction ID (auto-generated) |
| `token` | str | ❌ | Token type (auto-detected) |

**Returns:** Payment URL string

## How It Works

1. Validates Solana address format
2. Checks amount is between $0.01 and $10,000.00
3. Calls activation endpoint to check recipient's USDC status
4. Uses `usdcBasic` if activated, `usdcCreate` if not
5. Generates unique tracking ID
6. Returns complete payment URL

## Example Links

**$0.50 Demo:**
```
https://yatori.io/mobile/yatoriRequest?token=usdcBasic&to=4M4fd9JSEgrzbCko9uABWN1E1xhjxPsmMSt6KHf3ZjQ8&amount=0.50&yid=readme_demo_50c
```

## License

MIT — Built with 🔮 for the agent economy

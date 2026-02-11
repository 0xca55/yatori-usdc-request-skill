# Yatori Payment Link Generator

Generate USDC payment request links for the Yatori mobile payment system.

## Quick Start

```python
from yatori_link_generator import create_payment_link

# Generate a payment link
link = create_payment_link(
    recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
    amount=5.0,  # $5.00 USDC
    yid="optional_custom_id"  # Or auto-generated
)

print(link)
# https://yatori.io/mobile/yatoriRequest?token=usdcBasic&to=GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5&amount=5.00&yid=abc123xyz
```

## Features

- ✅ **Simple API** - One function to generate links
- ✅ **Auto-generated IDs** - Random unique yids (or provide your own)
- ✅ **Address Validation** - Checks Solana addresses
- ✅ **Amount Limits** - $0.01 minimum, $10,000.00 maximum
- ✅ **USDC Account Detection** - Auto-detects if recipient has USDC activated
- ✅ **Smart Token Selection** - Uses `usdcBasic` if activated, `usdcCreate` if not

## Installation

```bash
cp skill-yatori-link/ ~/.openclaw/skills/
```

## Usage Examples

### Request Payment from Someone
```python
# Someone owes you $10
link = create_payment_link(
    recipient="YOUR_WALLET_ADDRESS",
    amount=10.0,
    memo="Payment for services"
)

# Share the link via Telegram, email, etc.
send_message(f"Please pay here: {link}")
```

### Generate Link for Invoice
```python
# Create invoice link with custom ID for tracking
link = create_payment_link(
    recipient="YOUR_WALLET_ADDRESS",
    amount=50.0,
    yid=f"invoice_{customer_id}_{timestamp}"
)
```

### Agent-to-Agent Payments
```python
# One agent requesting payment from another
link = create_payment_link(
    recipient=requesting_agent_wallet,
    amount=calculated_fee,
    yid=f"agent_fee_{job_id}"
)
```

## Configuration

Set in your `.env`:
```bash
YATORI_BASE_URL=https://yatori.io/mobile/yatoriRequest
DEFAULT_TOKEN=usdcBasic
```

## API Reference

### `create_payment_link(recipient, amount, yid=None, token=None, network="mainnet-beta")`

**Parameters:**
- `recipient` (str): Solana wallet address (44 chars)
- `amount` (float): Amount in USDC dollars (e.g., 5.0 = $5.00)
  - **Minimum:** $0.01 USDC
  - **Maximum:** $10,000.00 USDC
- `yid` (str, optional): Unique transaction ID. Auto-generated if not provided
- `token` (str, optional): Token type. **Auto-detected** if not provided:
  - `usdcBasic` - Used if recipient already has USDC account activated
  - `usdcCreate` - Used if recipient needs USDC account created
- `network` (str, optional): Solana network. Default: "mainnet-beta"

**Returns:**
- `str`: Complete payment URL

**Example:**
```python
link = create_payment_link(
    recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
    amount=5.0
)
# Returns: https://yatori.io/mobile/yatoriRequest?token=usdcBasic&to=GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5&amount=5.00&yid=a7f3k2m9
```

## How It Works

1. **Address Validation** - Ensures recipient is valid Solana address (32-44 chars, base58)
2. **Amount Validation** - Validates amount is between $0.01 and $10,000.00 USDC
3. **USDC Account Check** - Calls activation endpoint to check if recipient has USDC account
4. **Token Selection** - Uses `usdcBasic` if activated, `usdcCreate` if account needs creation
5. **Amount Formatting** - Converts to proper decimal format (2 decimal places)
6. **ID Generation** - Creates random 10-char alphanumeric yid for tracking
7. **URL Construction** - Builds the complete payment link
8. **Return** - Ready-to-share URL

## Security Notes

- ⚠️ Generated links are **payment requests**, not signed transactions
- ⚠️ Anyone with the link can see the recipient and amount
- ✅ Use unique yids for tracking and preventing replay
- ✅ Links expire based on Yatori's server policy

## Troubleshooting

**Invalid address error:**
- Ensure Solana address is 32-44 characters
- Must be base58 encoded

**Amount issues:**
- Use decimal format (5.0 not 5)
- Minimum amount: $0.01 USDC
- Maximum amount: $10,000.00 USDC
- Error will specify exact issue

**Link not working:**
- Check Yatori service status
- Verify recipient has Yatori wallet set up
- If `usdcCreate` token used, recipient may need to accept account creation

**USDC Account Activation Check Failed:**
- Skill will default to `usdcCreate` token type
- Link will still work but may require recipient to approve account creation

## Related

- [Yatori Documentation](https://docs.yatori.io)
- [Solana Address Format](https://docs.solana.com/cli/transfer-tokens)
- [USDC on Solana](https://www.circle.com/en/usdc/multichain/solana)

---

Built with 🔮 for the agent economy
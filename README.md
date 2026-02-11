# Yatori USDC Payment Link Generator

[![Skill](https://img.shields.io/badge/Skill-Yatori-blue)](https://yatori.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Generate USDC payment request links for the [Yatori](https://yatori.io) mobile payment system.

## 🎯 Quick Example

Here's a live payment link — **send $0.50 USDC to test it out:**

### 👉 [**Pay $0.50 USDC**](https://yatori.io/mobile/yatoriRequest?token=usdcBasic&to=4M4fd9JSEgrzbCko9uABWN1E1xhjxPsmMSt6KHf3ZjQ8&amount=0.50&yid=readme_demo_50c)

```
https://yatori.io/mobile/yatoriRequest?token=usdcBasic&to=4M4fd9JSEgrzbCko9uABWN1E1xhjxPsmMSt6KHf3ZjQ8&amount=0.50&yid=readme_demo_50c
```

*Click the link above on mobile to open the Yatori payment flow!*

---

## ✨ Features

- 💳 **Smart Token Detection** — Automatically detects if recipient needs `usdcBasic` or `usdcCreate`
- 🔒 **Address Validation** — Validates Solana addresses before generating links
- 💰 **Amount Limits** — Enforces $0.01 minimum and $10,000.00 maximum
- 🆔 **Auto-Generated IDs** — Creates unique tracking IDs (or use your own)
- 🔗 **Simple API** — One function call to generate payment URLs

---

## 🚀 Installation

```bash
# Clone the skill
git clone https://github.com/0xca55/yatori-usdc-request-skill.git

# Copy to your OpenClaw skills directory
cp -r yatori-usdc-request-skill ~/.openclaw/skills/skill-yatori-link
```

---

## 📖 Usage

```python
from yatori_link_generator import create_payment_link

# Generate a payment link
link = create_payment_link(
    recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
    amount=5.0  # $5.00 USDC
)

print(link)
# Output: https://yatori.io/mobile/yatoriRequest?token=usdcBasic...
```

### Amount Validation

```python
# ✅ Valid amounts
create_payment_link(recipient, 0.01)      # Minimum
create_payment_link(recipient, 50.0)      # Standard
create_payment_link(recipient, 9999.99)   # Maximum

# ❌ These will raise ValueError
create_payment_link(recipient, 0.005)     # Too small
create_payment_link(recipient, 15000)     # Too large
```

### Automatic USDC Account Detection

The skill automatically checks if the recipient's USDC account is activated:

- **`usdcBasic`** — Used when recipient already has a USDC token account
- **`usdcCreate`** — Used when recipient needs a USDC account created (first-time receiver)

```python
# Token type auto-detected based on recipient status
link = create_payment_link(recipient="activated_wallet", amount=10.0)
# → token=usdcBasic

link = create_payment_link(recipient="new_wallet", amount=10.0)
# → token=usdcCreate
```

---

## 🔧 API Reference

### `create_payment_link(recipient, amount, yid=None, token=None, network="mainnet-beta")`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `recipient` | str | ✅ | Solana wallet address (32-44 chars, base58) |
| `amount` | float | ✅ | Amount in USDC ($0.01 - $10,000.00) |
| `yid` | str | ❌ | Unique transaction ID (auto-generated if omitted) |
| `token` | str | ❌ | Token type (auto-detected: `usdcBasic` or `usdcCreate`) |
| `network` | str | ❌ | Solana network (default: `mainnet-beta`) |

**Returns:** `str` — Complete payment URL

---

## 🧪 Testing

Try the live demo link above or run the tests:

```bash
python3 yatori_link_generator.py
```

---

## 🏗️ How It Works

1. **Validate Address** — Ensures recipient is a valid Solana address
2. **Check Amount** — Validates $0.01 ≤ amount ≤ $10,000.00
3. **Check Activation** — Calls Yatori endpoint to check USDC account status
4. **Select Token** — Uses `usdcBasic` if activated, `usdcCreate` if not
5. **Generate ID** — Creates random 10-char alphanumeric tracking ID
6. **Build URL** — Constructs the complete payment link

---

## 🔗 Links

- 🌐 [Yatori Website](https://yatori.io)
- 📚 [Skill Documentation](SKILL.md)
- 💻 [OpenClaw](https://github.com/openclaw/openclaw)

---

Built with 🔮 for the agent economy

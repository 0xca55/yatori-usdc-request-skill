"""
Yatori USDC Request Skill
Generate USDC payment request links for Yatori mobile payments

Usage:
    from skill import create_payment_link
    
    link = create_payment_link(
        recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
        amount=5.0
    )
    print(link)
    # https://yatori.io/mobile/yatoriRequest?token=usdcBasic...
"""

import secrets
import string
import re
import requests
from typing import Optional
from urllib.parse import urlencode


def validate_solana_address(address: str) -> bool:
    """Validate a Solana address (base58, 32-44 chars)."""
    if not address or len(address) < 32 or len(address) > 44:
        return False
    base58_alphabet = set('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
    return all(c in base58_alphabet for c in address)


def generate_yid(length: int = 10) -> str:
    """Generate a random unique transaction ID."""
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def format_amount(amount: float) -> str:
    """Format amount to 2 decimal places for USDC."""
    return f"{amount:.2f}"


def check_usdc_account_activation(address: str, network: str = "mainnet-beta") -> dict:
    """Check if a USDC token account is activated for the given address."""
    try:
        response = requests.post(
            "https://yumi-muddy-darkness-7179.fly.dev/is-usdc-acct-activated",
            json={"address": address, "network": network},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"isActivated": False, "error": str(e), "status": "Check failed"}


def validate_amount_range(amount: float) -> None:
    """Validate amount is within acceptable range ($0.01 to $10,000.00)."""
    MIN_AMOUNT = 0.01
    MAX_AMOUNT = 10000.00
    
    if amount < MIN_AMOUNT:
        raise ValueError(f"Amount must be at least ${MIN_AMOUNT:.2f} USDC, got ${amount}")
    
    if amount > MAX_AMOUNT:
        raise ValueError(f"Amount must be under ${MAX_AMOUNT:.2f} USDC, got ${amount}")


def create_payment_link(
    recipient: str,
    amount: float,
    yid: Optional[str] = None,
    token: Optional[str] = None,
    base_url: str = "https://yatori.io/mobile/yatoriRequest",
    network: str = "mainnet-beta"
) -> str:
    """
    Create a Yatori payment request link.
    
    Automatically checks if recipient's USDC account is activated and
    uses appropriate token type (usdcBasic or usdcCreate).
    
    Args:
        recipient: Solana wallet address to receive payment
        amount: Amount in USDC dollars ($0.01 to $10,000.00)
        yid: Optional unique transaction ID (auto-generated if not provided)
        token: Optional token type (auto-detected if not provided)
        base_url: Base URL for Yatori requests
        network: Solana network (default: mainnet-beta)
        
    Returns:
        Complete payment URL
        
    Raises:
        ValueError: If recipient address is invalid or amount is out of range
    """
    # Validate recipient address
    if not validate_solana_address(recipient):
        raise ValueError(f"Invalid Solana address: {recipient}")
    
    # Validate amount range
    validate_amount_range(amount)
    
    # Check USDC account activation status
    activation_check = check_usdc_account_activation(recipient, network)
    is_activated = activation_check.get("isActivated", False)
    
    # Determine token type
    if token is None:
        token = "usdcBasic" if is_activated else "usdcCreate"
    
    # Generate yid if not provided
    if yid is None:
        yid = generate_yid()
    
    # Build query parameters
    params = {
        "token": token,
        "to": recipient,
        "amount": format_amount(amount),
        "yid": yid
    }
    
    # Construct URL
    query_string = urlencode(params)
    return f"{base_url}?{query_string}"


def create_payment_link_with_tracking(
    recipient: str,
    amount: float,
    prefix: Optional[str] = None,
    token: Optional[str] = None,
    network: str = "mainnet-beta"
) -> dict:
    """
    Create a payment link with tracking information.
    
    Returns a dictionary with the link and metadata for tracking.
    """
    from datetime import datetime
    
    # Generate yid with optional prefix
    random_part = generate_yid(8)
    yid = f"{prefix}{random_part}" if prefix else random_part
    
    # Create the link
    url = create_payment_link(recipient, amount, yid, token, network=network)
    
    # Return with metadata
    return {
        "url": url,
        "yid": yid,
        "recipient": recipient,
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "token": token or ("usdcBasic" if check_usdc_account_activation(recipient, network).get("isActivated") else "usdcCreate")
    }


if __name__ == "__main__":
    # Test the skill
    print("🧪 Testing Yatori USDC Request Skill...")
    print()
    
    # Test 1: Valid payment link
    try:
        link = create_payment_link(
            recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
            amount=5.0
        )
        print(f"✅ Test 1 PASSED: Generated link")
        print(f"   {link[:70]}...")
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
    
    print()
    
    # Test 2: Amount validation
    try:
        create_payment_link("GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5", 0.005)
        print("❌ Test 2 FAILED: Should have rejected small amount")
    except ValueError:
        print("✅ Test 2 PASSED: Correctly rejected amount below minimum")
    
    print()
    print("🎉 Skill ready to use!")

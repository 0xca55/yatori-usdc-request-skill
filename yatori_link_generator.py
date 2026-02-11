"""
Yatori Payment Link Generator
Generate USDC payment request links for Yatori mobile payments
"""

import secrets
import string
import re
import requests
from typing import Optional
from urllib.parse import urlencode, urlunparse


def validate_solana_address(address: str) -> bool:
    """
    Validate a Solana address.
    
    Solana addresses are base58 encoded and typically 32-44 characters.
    """
    if not address or len(address) < 32 or len(address) > 44:
        return False
    
    # Base58 alphabet
    base58_alphabet = set('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
    
    # Check all characters are valid base58
    if not all(c in base58_alphabet for c in address):
        return False
    
    return True


def generate_yid(length: int = 10) -> str:
    """
    Generate a random unique transaction ID.
    
    Args:
        length: Length of the ID (default: 10)
        
    Returns:
        Random alphanumeric string
    """
    # Use secrets for cryptographically secure random generation
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def format_amount(amount: float) -> str:
    """
    Format amount to 2 decimal places for USDC.
    
    Args:
        amount: Amount in USDC dollars
        
    Returns:
        Formatted amount string
    """
    return f"{amount:.2f}"


def check_usdc_account_activation(address: str, network: str = "mainnet-beta") -> dict:
    """
    Check if a USDC token account is activated for the given address.
    
    Args:
        address: Solana wallet address
        network: Solana network (default: mainnet-beta)
        
    Returns:
        Dictionary with isActivated status and other info
    """
    try:
        response = requests.post(
            "https://yumi-muddy-darkness-7179.fly.dev/is-usdc-acct-activated",
            json={
                "address": address,
                "network": network
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # If check fails, assume not activated for safety
        return {
            "isActivated": False,
            "error": str(e),
            "status": "Check failed"
        }


def validate_amount_range(amount: float) -> None:
    """
    Validate amount is within acceptable range ($0.01 to $10,000.00).
    
    Args:
        amount: Amount in USDC dollars
        
    Raises:
        ValueError: If amount is outside valid range
    """
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
        amount: Amount in USDC dollars (e.g., 5.0 for $5.00)
               Must be between $0.01 and $10,000.00
        yid: Optional unique transaction ID (auto-generated if not provided)
        token: Optional token type (auto-detected if not provided)
        base_url: Base URL for Yatori requests
        network: Solana network (default: mainnet-beta)
        
    Returns:
        Complete payment URL
        
    Raises:
        ValueError: If recipient address is invalid or amount is out of range
        
    Example:
        >>> link = create_payment_link(
        ...     recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
        ...     amount=5.0
        ... )
        >>> print(link)
        https://yatori.io/mobile/yatoriRequest?token=usdcBasic&to=GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5&amount=5.00&yid=a7f3k2m9
    """
    # Validate recipient address
    if not validate_solana_address(recipient):
        raise ValueError(f"Invalid Solana address: {recipient}")
    
    # Validate amount range ($0.01 to $10,000.00)
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
    url = f"{base_url}?{query_string}"
    
    return url


def create_payment_link_with_tracking(
    recipient: str,
    amount: float,
    prefix: Optional[str] = None,
    token: str = "usdcBasic"
) -> dict:
    """
    Create a payment link with tracking information.
    
    Returns a dictionary with the link and metadata for tracking.
    
    Args:
        recipient: Solana wallet address
        amount: Amount in USDC
        prefix: Optional prefix for the yid (e.g., "invoice_123_")
        token: Token type
        
    Returns:
        Dictionary with 'url', 'yid', 'recipient', 'amount', 'timestamp'
    """
    from datetime import datetime
    
    # Generate yid with optional prefix
    random_part = generate_yid(8)
    yid = f"{prefix}{random_part}" if prefix else random_part
    
    # Create the link
    url = create_payment_link(recipient, amount, yid, token)
    
    # Return with metadata
    return {
        "url": url,
        "yid": yid,
        "recipient": recipient,
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "token": token
    }


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Simple payment link
    link = create_payment_link(
        recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
        amount=5.0
    )
    print(f"Simple link: {link}")
    
    # Example 2: With custom yid
    link = create_payment_link(
        recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
        amount=10.50,
        yid="invoice_123_abc"
    )
    print(f"Custom yid: {link}")
    
    # Example 3: With tracking
    result = create_payment_link_with_tracking(
        recipient="GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5",
        amount=25.00,
        prefix="agent_payment_"
    )
    print(f"\nWith tracking:")
    print(f"  URL: {result['url']}")
    print(f"  YID: {result['yid']}")
    print(f"  Amount: ${result['amount']}")
    print(f"  Time: {result['timestamp']}")
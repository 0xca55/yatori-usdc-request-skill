#!/usr/bin/env python3
"""
Example: Cass using the Yatori Link Generator Skill

This shows how I (Cass) would use this skill when you ask me
to create a payment link.
"""

from yatori_link_generator import create_payment_link, create_payment_link_with_tracking

# Your wallet address (from our setup)
MY_WALLET = "4M4fd9JSEgrzbCko9uABWN1E1xhjxPsmMSt6KHf3ZjQ8"

def generate_payment_request(recipient_address: str, amount_dollars: float, description: str = ""):
    """
    When you or someone else asks me to create a payment link,
    I use this function to generate it.
    """
    
    # Create the payment link
    link = create_payment_link(
        recipient=recipient_address,
        amount=amount_dollars,
        yid=f"cass_req_{description[:10]}" if description else None
    )
    
    return {
        "link": link,
        "amount": amount_dollars,
        "recipient": recipient_address,
        "note": f"Send ${amount_dollars} to this address"
    }


# Example scenarios:

print("=" * 60)
print("YATORI PAYMENT LINK GENERATOR - USAGE EXAMPLES")
print("=" * 60)

# Scenario 1: You ask me "send $5 to this address"
print("\n💬 You: 'Cass, create a payment link for $5 to send to Will'")
recipient = "GvCoHGGBR97Yphzc6SrRycZyS31oUYBM8m9hLRtJT7r5"  # Example address
result = generate_payment_request(recipient, 5.0, "will_payment")
print(f"🔗 Link: {result['link']}")

# Scenario 2: Someone asks me to pay them
print("\n💬 Someone: 'Can you pay me $10 for the service?'")
my_link = create_payment_link(
    recipient=MY_WALLET,  # Your wallet receives payment
    amount=10.0,
    yid="service_payment_feb11"
)
print(f"🔗 Payment Link: {my_link}")
print(f"   Share this link with them to pay you $10")

# Scenario 3: Agent-to-agent payment
print("\n💬 Agent request: 'Request $2.50 for API usage'")
api_payment = create_payment_link_with_tracking(
    recipient=MY_WALLET,
    amount=2.50,
    prefix="api_usage_"
)
print(f"🔗 Link: {api_payment['url']}")
print(f"   YID: {api_payment['yid']} (for tracking)")

print("\n" + "=" * 60)
print("SKILL READY TO USE!")
print("=" * 60)
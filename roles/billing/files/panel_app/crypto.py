import os, httpx
API_BASE = "https://api.cryptocloud.plus"
API_KEY = os.getenv("CRYPTOCLOUD_API_KEY") or ""
SHOP_ID = os.getenv("CRYPTOCLOUD_SHOP_ID") or ""

def cryptocloud_create_invoice(amount: float, currency: str = "USD", description: str = ""):
    url = f"{API_BASE}/v1/invoice/create"
    payload = {"shop_id": SHOP_ID, "amount": str(amount), "currency": currency, "description": description}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    with httpx.Client(timeout=15.0) as client:
        r = client.post(url, json=payload, headers=headers, verify=False)
        r.raise_for_status()
        return r.json()

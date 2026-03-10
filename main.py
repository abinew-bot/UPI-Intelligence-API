from fastapi import FastAPI, Header
import re
import json

app = FastAPI()

API_KEYS = [
    "test123",
    "dev456"
]

RATE_LIMIT = 100


# -----------------------------
# Merchant Database Functions
# -----------------------------
def load_merchants():
    with open("merchant_db.json", "r") as f:
        return json.load(f)


def save_merchants(data):
    with open("merchant_db.json", "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# Usage Database Functions
# -----------------------------
def load_usage():
    with open("usage_db.json", "r") as f:
        return json.load(f)


def save_usage(data):
    with open("usage_db.json", "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------
# Home Endpoint
# -----------------------------
@app.get("/")
def home():
    return {"message": "UPI Intelligence API running"}


# -----------------------------
# Main API Endpoint
# -----------------------------
@app.post("/parse_sms")
def parse_sms(text: str, api_key: str = Header(...)):

    # Authentication
    if api_key not in API_KEYS:
        return {"error": "Invalid API key"}

    # Load usage data
    usage = load_usage()

    if api_key not in usage:
        usage[api_key] = 0

    # Rate limiting
    if usage[api_key] >= RATE_LIMIT:
        return {"error": "Rate limit exceeded"}

    usage[api_key] += 1
    save_usage(usage)

    # Load merchants
    merchants = load_merchants()

    # Extract amount
    amount_match = re.findall(r'\d+', text)
    amount = amount_match[0] if amount_match else None

    merchant = "Unknown"
    category = "Other"

    text_lower = text.lower()

    # Known merchant detection
    for key in merchants:
        if key in text_lower:
            merchant = key
            category = merchants[key]
            break

    # Unknown merchant learning
    if merchant == "Unknown":

        words = text_lower.split()
        stop_words = ["paid", "to", "via", "upi", "from", "at"]

        for word in words:
            if word.isalpha() and word not in stop_words:
                merchant = word
                break

        merchants[merchant] = "Unknown"
        save_merchants(merchants)

    return {
        "amount": amount,
        "merchant": merchant,
        "category": category,
        "original_text": text
    }
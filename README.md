# UPI Transaction Parser API

Convert Indian UPI payment SMS into structured transaction data.

Example:

SMS:
₹450 paid to Amazon

API Response:
{
  "amount": 450,
  "merchant": "Amazon",
  "category": "Shopping"
}

---

## Why This API Exists

Fintech and expense tracking apps often receive transaction data as unstructured SMS text.

Example:

₹120 paid to Swiggy  
₹800 transferred to Rahul  
₹450 paid to Amazon  

Parsing this reliably requires building complex logic.

This API converts those messages into structured financial data instantly.

---

## Live API

API Documentation:

https://upi-intelligence-api.onrender.com/docs

---

## Example Request

POST request:
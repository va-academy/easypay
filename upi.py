
"""
EasyPay Finance - Sample UPI Payment API
Framework: Flask
Mode: DEMO ONLY — no real money transfers
"""

from flask import Flask, request, jsonify
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode
from uuid import uuid4
from datetime import datetime, timezone
import re

app = Flask(__name__)

# Demo storage only. Use a database in production.
payments = {}

MERCHANT_NAME = "EasyPay Finance"
MERCHANT_UPI_ID = "easypay@upi"  # Replace with an authorized merchant VPA


def utc_now():
    return datetime.now(timezone.utc).isoformat()


@app.route("/api/upi/payments", methods=["POST"])
def create_payment():
    data = request.get_json(silent=True) or {}

    upi_id = str(data.get("upi_id", "")).strip()
    description = str(data.get("description", "EasyPay Payment")).strip()

    # Basic VPA format check; not proof that the ID exists.
    if not re.fullmatch(r"[A-Za-z0-9._-]{2,256}@[A-Za-z0-9.-]{2,64}", upi_id):
        return jsonify({"error": "Invalid UPI ID format"}), 400

    try:
        amount = Decimal(str(data.get("amount", "")))
    except (InvalidOperation, ValueError):
        return jsonify({"error": "Invalid payment amount"}), 400

    if not amount.is_finite() or amount <= 0 or amount > Decimal("100000"):
        return jsonify({"error": "Amount must be between ₹0.01 and ₹100000"}), 400

    if len(description) > 100:
        return jsonify({"error": "Description is too long"}), 400

    payment_id = str(uuid4())

    # Creates a payment intent URI, not a completed transaction.
    upi_params = {
        "pa": MERCHANT_UPI_ID,
        "pn": MERCHANT_NAME,
        "am": f"{amount:.2f}",
        "cu": "INR",
        "tn": description,
        "tr": payment_id,
    }

    upi_uri = "upi://pay?" + urlencode(upi_params)

    payments[payment_id] = {
        "payment_id": payment_id,
        "customer_upi_id": upi_id,
        "amount": f"{amount:.2f}",
        "currency": "INR",
        "description": description,
        "status": "PENDING",
        "created_at": utc_now(),
    }

    return jsonify({
        "message": "UPI payment request created",
        "payment": payments[payment_id],
        "upi_uri": upi_uri,
        "note": "Payment is pending. Verify with your payment provider."
    }), 201


@app.route("/api/upi/payments/<payment_id>", methods=["GET"])
def get_payment_status(payment_id):
    payment = payments.get(payment_id)

    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify({"payment": payment}), 200


# TEST ONLY: Never expose this endpoint in production.
@app.route(
    "/api/test/payments/<payment_id>/status",
    methods=["POST"]
)
def simulate_payment_status(payment_id):
    payment = payments.get(payment_id)

    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    data = request.get_json(silent=True) or {}
    new_status = data.get("status")

    allowed_statuses = {"SUCCESS", "FAILED", "PENDING"}

    if new_status not in allowed_statuses:
        return jsonify({
            "error": "Status must be SUCCESS, FAILED, or PENDING"
        }), 400

    payment["status"] = new_status
    payment["updated_at"] = utc_now()

    return jsonify({
        "message": "Demo status updated",
        "payment": payment
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
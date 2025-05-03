import os
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from .config import PURCHASES_DIR
from .items import get_cached_items

purchases_bp = Blueprint("purchases", __name__)

@purchases_bp.route("/upload-purchases", methods=["POST"])
def upload_purchases():
    try:
        data = request.get_json()
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid data"}), 400

        enriched = []
        items = get_cached_items()
        for entry in data:
            item = next((i for i in items if i["id"] == entry["itemId"]), None)
            if not item:
                continue
            enriched.append({
                "itemId": item["id"],
                "name": item["name"],
                "stand": item.get("stand", "Okänt"),
                "price": item["price"],
                "quantity": entry.get("quantity", 1),
                "timestamp": entry.get("timestamp")
            })

        if not enriched:
            return jsonify({"error": "No valid purchases"}), 400

        filename = f"{datetime.now().strftime('%Y-%m-%d')}.json"
        path = os.path.join(PURCHASES_DIR, filename)

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        else:
            existing = []

        existing.extend(enriched)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        print(f"[✓] Sparade {len(enriched)} köp i {filename}")
        return "OK", 200

    except Exception as e:
        print(f"[✗] Fel vid synk: {e}")
        return jsonify({"error": "Serverfel"}), 500

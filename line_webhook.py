"""
Minimal Flask webhook to capture LINE userId/groupId/roomId.

How to use:
1) Install deps: `pip install flask` (and `pip install line-bot-sdk` if you later add verification)
2) Run: `python /Users/tetsu/cursor_for_stocks_info/line_webhook.py`
3) Expose locally with a tunnel (e.g., ngrok): `ngrok http 5000`
4) Set webhook URL in LINE Developers to: https://<your-ngrok-domain>/callback
5) Invite your bot to a chat or send a message to trigger events; IDs will be stored in recipients.txt.

Optional signature verification: set env LINE_CHANNEL_SECRET. If not set, the app will skip verification.
"""

from __future__ import annotations

import os
import json
from typing import Any, Dict

from flask import Flask, request, jsonify
import hmac
import hashlib
import base64


app = Flask(__name__)

RECIPIENTS_FILE = os.path.join(os.path.dirname(__file__), "recipients.txt")


def verify_signature(channel_secret: str, body: bytes, signature: str) -> bool:
    mac = hmac.new(channel_secret.encode("utf-8"), msg=body, digestmod=hashlib.sha256).digest()
    expected = base64.b64encode(mac).decode("utf-8")
    return hmac.compare_digest(expected, signature)


def save_recipient(identifier: str) -> None:
    identifier = identifier.strip()
    if not identifier:
        return
    # Append unique identifiers to recipients file
    existing: set[str] = set()
    if os.path.exists(RECIPIENTS_FILE):
        with open(RECIPIENTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                existing.add(line.strip())
    if identifier not in existing:
        with open(RECIPIENTS_FILE, "a", encoding="utf-8") as f:
            f.write(identifier + "\n")


@app.route("/health", methods=["GET"])  # simple health check
def health() -> Any:
    return jsonify({"status": "ok"})


@app.route("/recipients", methods=["GET"])  # view collected IDs
def recipients() -> Any:
    ids: list[str] = []
    if os.path.exists(RECIPIENTS_FILE):
        with open(RECIPIENTS_FILE, "r", encoding="utf-8") as f:
            ids = [line.strip() for line in f if line.strip()]
    return jsonify({"recipients": ids})


@app.route("/callback", methods=["POST"])  # LINE webhook endpoint
def callback() -> Any:
    body_bytes: bytes = request.get_data() or b""
    signature = request.headers.get("X-Line-Signature", "")
    channel_secret = os.getenv("LINE_CHANNEL_SECRET")

    if channel_secret:
        try:
            if not verify_signature(channel_secret, body_bytes, signature):
                return ("signature verification failed", 400)
        except Exception:
            return ("signature verification error", 400)

    try:
        payload: Dict[str, Any] = json.loads(body_bytes.decode("utf-8"))
    except Exception:
        return ("invalid json", 400)

    events = payload.get("events", []) or []
    for event in events:
        source = event.get("source", {}) or {}
        # Order: userId > groupId > roomId
        for key in ("userId", "groupId", "roomId"):
            if key in source and source[key]:
                save_recipient(source[key])
                break

    return ("ok", 200)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)




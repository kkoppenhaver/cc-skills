#!/usr/bin/env python3
"""
Kit Broadcast API Script

Creates and schedules email broadcasts via the Kit (ConvertKit) API v4.

Usage:
    python kit_broadcast.py --subject "Subject line" --content "<p>HTML content</p>" --send-at "2026-01-20T10:00:00-06:00"
    python kit_broadcast.py --subject "Subject line" --content "<p>HTML content</p>" --draft  # Creates draft only
    python kit_broadcast.py --dry-run --subject "Test" --content "<p>Test</p>" --send-at "2026-01-20T10:00:00-06:00"

Environment:
    KIT_API_KEY: Your Kit API key (required)
"""

import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError


CC4M_TAG_ID = 14154457  # "CC4M" tag for Claude Code for Marketers subscribers


def create_broadcast(
    subject: str,
    content: str,
    send_at: str | None = None,
    preview_text: str | None = None,
    description: str | None = None,
    dry_run: bool = False
) -> dict:
    """Create a broadcast in Kit.

    Args:
        subject: Email subject line
        content: HTML content of the email
        send_at: ISO8601 timestamp for scheduled send (None = draft)
        preview_text: Preview text shown in email clients
        description: Internal description of the broadcast
        dry_run: If True, print request but don't send

    Returns:
        API response as dict
    """
    api_key = os.environ.get("KIT_API_KEY")
    if not api_key:
        print("Error: KIT_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    url = "https://api.kit.com/v4/broadcasts"

    payload = {
        "subject": subject,
        "content": content,
        "public": False,  # Don't publish to web
        "subscriber_filter": [{
            "all": [{"type": "tag", "ids": [CC4M_TAG_ID]}]
        }]
    }

    if send_at:
        payload["send_at"] = send_at

    if preview_text:
        payload["preview_text"] = preview_text

    if description:
        payload["description"] = description

    if dry_run:
        print("=== DRY RUN ===")
        print(f"URL: POST {url}")
        print(f"Headers: X-Kit-Api-Key: {api_key[:10]}...")
        print(f"Payload:\n{json.dumps(payload, indent=2)}")
        return {"dry_run": True, "payload": payload}

    headers = {
        "Content-Type": "application/json",
        "X-Kit-Api-Key": api_key
    }

    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers=headers, method="POST")

    try:
        with urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Create Kit email broadcasts")
    parser.add_argument("--subject", required=True, help="Email subject line")
    parser.add_argument("--content", required=True, help="HTML content of the email")
    parser.add_argument("--send-at", help="ISO8601 timestamp to schedule (omit for draft)")
    parser.add_argument("--preview-text", help="Preview text for email clients")
    parser.add_argument("--description", help="Internal description")
    parser.add_argument("--dry-run", action="store_true", help="Print request without sending")

    args = parser.parse_args()

    result = create_broadcast(
        subject=args.subject,
        content=args.content,
        send_at=args.send_at,
        preview_text=args.preview_text,
        description=args.description,
        dry_run=args.dry_run
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

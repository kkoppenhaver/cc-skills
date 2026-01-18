#!/usr/bin/env python3
"""
Typefully Tweet Scheduler

Schedule tweets via the Typefully API v2.

Required environment variables:
  TYPEFULLY_API_KEY        - API key from Typefully Settings > API & Integrations
  TYPEFULLY_SOCIAL_SET_ID  - Social set ID (run with --list-social-sets to find it)
"""

import json
import os
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any


API_BASE = "https://api.typefully.com/v2"


@dataclass
class ScheduleResult:
    success: bool
    draft_id: Optional[str] = None
    status: Optional[str] = None
    scheduled_date: Optional[str] = None
    share_url: Optional[str] = None
    error: Optional[str] = None


class TypefullyScheduler:
    def __init__(self, api_key: str, social_set_id: str):
        self.api_key = api_key
        self.social_set_id = social_set_id

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make an authenticated request to the Typefully API."""
        url = f"{API_BASE}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        body = json.dumps(data).encode() if data else None
        request = urllib.request.Request(url, data=body, headers=headers, method=method)

        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else str(e)
            try:
                error_data = json.loads(error_body)
                raise Exception(f"API Error ({e.code}): {error_data.get('message', error_body)}")
            except json.JSONDecodeError:
                raise Exception(f"API Error ({e.code}): {error_body}")

    def list_social_sets(self) -> List[Dict[str, Any]]:
        """List all available social sets."""
        response = self._make_request("GET", "/social-sets")
        return response.get("data", [])

    def schedule_tweet(
        self,
        text: str,
        publish_at: str = "next-free-slot",
        share: bool = False
    ) -> ScheduleResult:
        """
        Schedule a tweet via Typefully.

        Args:
            text: The tweet text
            publish_at: When to publish - "now", "next-free-slot", or ISO 8601 datetime
            share: Whether to generate a public share URL

        Returns:
            ScheduleResult with draft details or error
        """
        data = {
            "platforms": {
                "x": {
                    "enabled": True,
                    "posts": [{"text": text}]
                }
            },
            "publish_at": publish_at,
            "share": share
        }

        try:
            response = self._make_request(
                "POST",
                f"/social-sets/{self.social_set_id}/drafts",
                data
            )

            return ScheduleResult(
                success=True,
                draft_id=response.get("id"),
                status=response.get("status"),
                scheduled_date=response.get("scheduled_date"),
                share_url=response.get("share_url")
            )
        except Exception as e:
            return ScheduleResult(success=False, error=str(e))

    def schedule_thread(
        self,
        posts: List[str],
        publish_at: str = "next-free-slot",
        share: bool = False
    ) -> ScheduleResult:
        """
        Schedule a thread via Typefully.

        Args:
            posts: List of tweet texts (each becomes a post in the thread)
            publish_at: When to publish - "now", "next-free-slot", or ISO 8601 datetime
            share: Whether to generate a public share URL

        Returns:
            ScheduleResult with draft details or error
        """
        data = {
            "platforms": {
                "x": {
                    "enabled": True,
                    "posts": [{"text": text} for text in posts]
                }
            },
            "publish_at": publish_at,
            "share": share
        }

        try:
            response = self._make_request(
                "POST",
                f"/social-sets/{self.social_set_id}/drafts",
                data
            )

            return ScheduleResult(
                success=True,
                draft_id=response.get("id"),
                status=response.get("status"),
                scheduled_date=response.get("scheduled_date"),
                share_url=response.get("share_url")
            )
        except Exception as e:
            return ScheduleResult(success=False, error=str(e))


def format_result(result: ScheduleResult) -> str:
    """Format a schedule result for display."""
    lines = []

    if result.success:
        lines.append("Tweet scheduled successfully")
        if result.draft_id:
            lines.append(f"   Draft ID: {result.draft_id}")
        if result.status:
            lines.append(f"   Status: {result.status}")
        if result.scheduled_date:
            lines.append(f"   Scheduled: {result.scheduled_date}")
        if result.share_url:
            lines.append(f"   Share URL: {result.share_url}")
    else:
        lines.append(f"Failed to schedule tweet")
        if result.error:
            lines.append(f"   Error: {result.error}")

    return "\n".join(lines)


def format_social_sets(social_sets: List[Dict[str, Any]]) -> str:
    """Format social sets for display."""
    if not social_sets:
        return "No social sets found."

    lines = ["Available Social Sets:\n"]
    for ss in social_sets:
        lines.append(f"   ID: {ss.get('id')}")
        lines.append(f"   Name: {ss.get('name', 'Unnamed')}")

        accounts = ss.get("accounts", [])
        if accounts:
            platforms = [f"{a.get('platform', '?')}/@{a.get('username', '?')}" for a in accounts]
            lines.append(f"   Accounts: {', '.join(platforms)}")
        lines.append("")

    return "\n".join(lines)


def get_env_or_exit(name: str) -> str:
    """Get an environment variable or exit with an error."""
    value = os.environ.get(name)
    if not value:
        print(f"Error: {name} environment variable is not set.")
        print(f"\nTo set it, run:")
        print(f"  export {name}=your_value_here")
        sys.exit(1)
    return value


def main():
    print("Typefully Tweet Scheduler\n")

    # Check for --list-social-sets flag
    if len(sys.argv) > 1 and sys.argv[1] == "--list-social-sets":
        api_key = get_env_or_exit("TYPEFULLY_API_KEY")
        scheduler = TypefullyScheduler(api_key, "")

        try:
            social_sets = scheduler.list_social_sets()
            print(format_social_sets(social_sets))
        except Exception as e:
            print(f"Error fetching social sets: {e}")
            sys.exit(1)
        return

    # Normal scheduling flow
    api_key = get_env_or_exit("TYPEFULLY_API_KEY")
    social_set_id = get_env_or_exit("TYPEFULLY_SOCIAL_SET_ID")

    scheduler = TypefullyScheduler(api_key, social_set_id)

    # Get tweet text
    print("Enter your tweet (or 'thread' for multi-post thread):")
    first_line = input("> ").strip()

    if first_line.lower() == "thread":
        print("\nEnter each post in the thread (empty line to finish):")
        posts = []
        i = 1
        while True:
            post = input(f"Post {i}: ").strip()
            if not post:
                break
            posts.append(post)
            i += 1

        if not posts:
            print("No posts entered. Exiting.")
            return

        text = None
        is_thread = True
    else:
        text = first_line
        posts = None
        is_thread = False

    # Get scheduling option
    print("\nWhen to publish?")
    print("  1. Next free slot (Typefully auto-schedules)")
    print("  2. Publish now")
    print("  3. Specific date/time")

    choice = input("\nChoice (1-3): ").strip()

    if choice == "2":
        publish_at = "now"
    elif choice == "3":
        print("\nEnter date/time in ISO 8601 format")
        print("Example: 2025-01-20T14:00:00Z")
        publish_at = input("> ").strip()
    else:
        publish_at = "next-free-slot"

    # Generate share URL?
    share_input = input("\nGenerate share URL? (y/N): ").strip().lower()
    share = share_input == "y"

    # Schedule
    print("\nScheduling...")

    if is_thread:
        result = scheduler.schedule_thread(posts, publish_at, share)
    else:
        result = scheduler.schedule_tweet(text, publish_at, share)

    print("\n" + format_result(result))


if __name__ == "__main__":
    main()

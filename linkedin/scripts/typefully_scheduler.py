#!/usr/bin/env python3
"""
Typefully LinkedIn Scheduler

Schedule posts to LinkedIn via the Typefully API v2.

Required environment variables:
  TYPEFULLY_API_KEY      - API key from Typefully Settings > API & Integrations
  TYPEFULLY_SOCIAL_SET_ID - Social set ID (run with --list-social-sets to find it)

Usage:
  # Schedule a post from a file
  python typefully_scheduler.py --file /path/to/post.txt --schedule next-free-slot

  # Schedule for a specific time
  python typefully_scheduler.py --file /path/to/post.txt --schedule 2026-01-20T18:00:00Z

  # Publish immediately
  python typefully_scheduler.py --file /path/to/post.txt --schedule now

  # Show currently scheduled posts
  python typefully_scheduler.py --list-scheduled

  # List social sets
  python typefully_scheduler.py --list-social-sets
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass
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
        return response.get("results", [])

    def get_social_set_details(self, social_set_id: str) -> Dict[str, Any]:
        """Get detailed info about a social set including connected platforms."""
        return self._make_request("GET", f"/social-sets/{social_set_id}/")

    def list_scheduled_drafts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List scheduled drafts, sorted by scheduled date."""
        response = self._make_request(
            "GET",
            f"/social-sets/{self.social_set_id}/drafts?limit={limit}"
        )
        drafts = response.get("results", [])
        # Filter to only scheduled posts and sort by date
        scheduled = [d for d in drafts if d.get("status") == "scheduled" and d.get("scheduled_date")]
        scheduled.sort(key=lambda d: d.get("scheduled_date", ""))
        return scheduled

    def schedule_post(
        self,
        text: str,
        publish_at: str = "next-free-slot",
        share: bool = False
    ) -> ScheduleResult:
        """
        Schedule a LinkedIn post via Typefully.

        Args:
            text: The post text
            publish_at: When to publish - "now", "next-free-slot", or ISO 8601 datetime
            share: Whether to generate a public share URL

        Returns:
            ScheduleResult with draft details or error
        """
        data = {
            "platforms": {
                "linkedin": {
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


def format_result(result: ScheduleResult) -> str:
    """Format a schedule result for display."""
    lines = []

    if result.success:
        lines.append("LinkedIn post scheduled successfully")
        if result.draft_id:
            lines.append(f"   Draft ID: {result.draft_id}")
        if result.status:
            lines.append(f"   Status: {result.status}")
        if result.scheduled_date:
            lines.append(f"   Scheduled: {result.scheduled_date}")
        if result.share_url:
            lines.append(f"   Share URL: {result.share_url}")
    else:
        lines.append("Failed to schedule LinkedIn post")
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
        if ss.get('username'):
            lines.append(f"   Username: @{ss.get('username')}")
        lines.append("")

    return "\n".join(lines)


def format_social_set_details(details: Dict[str, Any]) -> str:
    """Format social set details for display."""
    lines = [f"Social Set: {details.get('name', 'Unnamed')} (ID: {details.get('id')})\n"]
    lines.append("Connected Platforms:")

    platforms = details.get("platforms", {})
    for name, info in platforms.items():
        if info:
            display_name = "X/Twitter" if name == "x" else name.title()
            lines.append(f"   {display_name}: @{info.get('username')} - {info.get('profile_url')}")

    return "\n".join(lines)


def format_scheduled_drafts(drafts: List[Dict[str, Any]]) -> str:
    """Format scheduled drafts for display."""
    if not drafts:
        return "No posts currently scheduled."

    lines = ["Currently scheduled posts:\n"]
    for draft in drafts:
        scheduled = draft.get("scheduled_date", "Unknown")
        preview = draft.get("preview", "")[:50]
        if len(draft.get("preview", "")) > 50:
            preview += "..."

        platforms = []
        if draft.get("x_post_enabled"):
            platforms.append("X")
        if draft.get("linkedin_post_enabled"):
            platforms.append("LinkedIn")
        platform_str = ", ".join(platforms) if platforms else "Unknown"

        lines.append(f"  {scheduled}  [{platform_str}]")
        lines.append(f"    {preview}")
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
    parser = argparse.ArgumentParser(
        description="Schedule LinkedIn posts via Typefully API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --file post.txt --schedule next-free-slot
  %(prog)s --file post.txt --schedule 2026-01-20T18:00:00Z
  %(prog)s --file post.txt --schedule now
  %(prog)s --list-scheduled
  %(prog)s --list-social-sets
        """
    )
    parser.add_argument("--file", "-f", help="Path to file containing post text")
    parser.add_argument("--schedule", "-s", default="next-free-slot",
                        help="When to publish: 'now', 'next-free-slot', or ISO 8601 datetime")
    parser.add_argument("--share", action="store_true", help="Generate a public share URL")
    parser.add_argument("--list-scheduled", action="store_true", help="List currently scheduled posts")
    parser.add_argument("--list-social-sets", action="store_true", help="List available social sets")
    parser.add_argument("--details", action="store_true", help="Show social set details")

    args = parser.parse_args()

    api_key = get_env_or_exit("TYPEFULLY_API_KEY")

    # Handle --list-social-sets
    if args.list_social_sets:
        scheduler = TypefullyScheduler(api_key, "")
        try:
            social_sets = scheduler.list_social_sets()
            print(format_social_sets(social_sets))
        except Exception as e:
            print(f"Error fetching social sets: {e}")
            sys.exit(1)
        return

    social_set_id = get_env_or_exit("TYPEFULLY_SOCIAL_SET_ID")
    scheduler = TypefullyScheduler(api_key, social_set_id)

    # Handle --details
    if args.details:
        try:
            details = scheduler.get_social_set_details(social_set_id)
            print(format_social_set_details(details))
        except Exception as e:
            print(f"Error fetching details: {e}")
            sys.exit(1)
        return

    # Handle --list-scheduled
    if args.list_scheduled:
        try:
            scheduled_drafts = scheduler.list_scheduled_drafts()
            print(format_scheduled_drafts(scheduled_drafts))
        except Exception as e:
            print(f"Error fetching scheduled posts: {e}")
            sys.exit(1)
        return

    # Schedule a post - requires --file
    if not args.file:
        parser.error("--file is required when scheduling a post")

    # Read post content from file
    try:
        with open(args.file, "r") as f:
            text = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    if not text:
        print("Error: Post file is empty")
        sys.exit(1)

    # Show currently scheduled posts for context
    try:
        scheduled_drafts = scheduler.list_scheduled_drafts()
        if scheduled_drafts:
            print(format_scheduled_drafts(scheduled_drafts))
            print()
    except Exception:
        pass  # Non-fatal, continue with scheduling

    # Schedule the post
    print(f"Scheduling LinkedIn post...")
    print(f"  Schedule: {args.schedule}")
    print(f"  Content preview: {text[:50]}{'...' if len(text) > 50 else ''}")
    print()

    result = scheduler.schedule_post(text, args.schedule, args.share)
    print(format_result(result))

    if not result.success:
        sys.exit(1)


if __name__ == "__main__":
    main()

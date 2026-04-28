from collections import defaultdict
from typing import Any

import requests
from utils.config import AppConfig

# =========================
# CLIENT
# =========================


class YouTrackClient:
    def __init__(self, config: AppConfig):
        self.base_url = config.youtrack.url
        self.headers = {
            "Authorization": f"Bearer {config.youtrack.token}",
            "Accept": "application/json",
        }
        self.sprint_prefix = config.youtrack.sprint_prefix
        self.story_points_field = config.youtrack.story_points_field

    # =========================
    # FETCH
    # =========================

    def fetch_issues(
        self,
        query: str | None = None,
        batch_size: int = 50,
        fields: str = "idReadable,tags(name),customFields(name,value)",
    ) -> list[dict[str, Any]]:
        all_issues = []
        skip = 0

        while True:
            params = {
                "fields": fields,
                "$top": batch_size,
                "$skip": skip,
            }

            if query:
                params["query"] = query

            response = requests.get(
                f"{self.base_url}/api/issues",
                headers=self.headers,
                params=params,
            )

            response.raise_for_status()
            batch = response.json()

            if not batch:
                break

            all_issues.extend(batch)
            skip += batch_size

            print(f"[YouTrack] fetched {len(all_issues)} issues")

        return all_issues

    # =========================
    # PARSING
    # =========================

    def get_sprint(self, issue: dict[str, Any]) -> str | None:
        for tag in issue.get("tags", []):
            name = tag.get("name")
            if name and name.startswith(self.sprint_prefix):
                return name
        return None

    def get_story_points(self, issue: dict[str, Any]) -> int | None:
        for field in issue.get("customFields", []):
            if field.get("name") == self.story_points_field:
                value = field.get("value")
                if isinstance(value, dict):
                    return value.get("name") or value.get("value")
                return value
        return None

    # =========================
    # AGGREGATION
    # =========================

    def build_throughput_items(self, issues: list[dict[str, Any]]) -> dict[str, int]:
        sprint_counts = defaultdict(int)

        for issue in issues:
            sprint = self.get_sprint(issue)
            if sprint:
                sprint_counts[sprint] += 1

        return dict(sprint_counts)

    def build_throughput_story_points(
        self, issues: list[dict[str, Any]]
    ) -> dict[str, int]:
        sprint_points = defaultdict(int)

        for issue in issues:
            sprint = self.get_sprint(issue)
            points = self.get_story_points(issue)

            if sprint and points:
                try:
                    sprint_points[sprint] += int(points)
                except (ValueError, TypeError):
                    pass

        return dict(sprint_points)

    # =========================
    # UTILS
    # =========================

    def sort_sprints(self, sprint_data: dict[str, int]) -> tuple[list[str], list[int]]:
        def sprint_key(s: str) -> int:
            return int(s.replace(self.sprint_prefix, ""))

        sorted_sprints = sorted(sprint_data.keys(), key=sprint_key)
        values = [sprint_data[s] for s in sorted_sprints]

        return sorted_sprints, values

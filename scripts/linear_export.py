#!/usr/bin/env python3
"""
Linear to CSV Export Script
Exports NIEMS Project issues from Linear and converts to CSV format

Usage:
    python linear_export.py --api-key YOUR_LINEAR_API_KEY --team STR

Environment Variables:
    LINEAR_API_KEY: Your Linear API key
    LINEAR_TEAM_ID: Team ID (default: STR)
"""

import os
import sys
import json
import csv
import re
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import requests


class LinearExporter:
    """Export Linear issues to CSV format"""
    
    def __init__(self, api_key: str, team_id: str = "STR"):
        self.api_key = api_key
        self.team_id = team_id
        self.api_url = "https://api.linear.app/graphql"
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
    
    def fetch_issues(self) -> List[Dict]:
        """Fetch all issues from Linear team"""
        query = """
        query($teamId: String!) {
          team(id: $teamId) {
            issues {
              nodes {
                id
                title
                description
                state { name }
                priority
                priorityLabel
                assignee { 
                  name 
                  email 
                }
                createdAt
                updatedAt
                dueDate
                project { name }
                labels {
                  nodes {
                    name
                  }
                }
              }
            }
          }
        }
        """
        
        variables = {"teamId": self.team_id}
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"query": query, "variables": variables}
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                raise Exception(f"Linear API errors: {data['errors']}")
            
            issues = data.get("data", {}).get("team", {}).get("issues", {}).get("nodes", [])
            print(f"✅ Fetched {len(issues)} issues from Linear")
            return issues
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching from Linear API: {e}")
            sys.exit(1)
    
    def extract_json_metadata(self, description: str) -> Optional[Dict]:
        """Extract JSON metadata from issue description"""
        if not description:
            return None
        
        # Look for <!-- METADATA_JSON ... --> pattern
        pattern = r'<!--\s*METADATA_JSON[^>]*?\n({.*?})\n-->'
        match = re.search(pattern, description, re.DOTALL)
        
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError as e:
                print(f"⚠️  Warning: Invalid JSON metadata - {e}")
                return None
        return None
    
    def parse_issue_title(self, title: str) -> Dict:
        """Parse issue title for [Type] [Region] [Year] pattern"""
        # Pattern: [Type] [Region] [Year] Project Name
        pattern = r'\[([^\]]+)\]\s*\[([^\]]+)\]\s*\[([^\]]+)\]\s*(.+)'
        match = re.match(pattern, title)
        
        if match:
            return {
                "type": match.group(1).lower(),
                "region": match.group(2).lower(),
                "year": match.group(3),
                "name": match.group(4).strip()
            }
        return {"name": title}
    
    def convert_to_csv_row(self, issue: Dict) -> Dict:
        """Convert Linear issue to CSV row format"""
        
        # Extract JSON metadata
        metadata = self.extract_json_metadata(issue.get("description", ""))
        
        # Parse title
        title_data = self.parse_issue_title(issue["title"])
        
        # Build CSV row
        row = {
            # Linear data
            "linear_id": issue["id"],
            "linear_url": f"https://linear.app/mande-niems/issue/{issue['id']}",
            "linear_state": issue["state"]["name"] if issue.get("state") else "",
            "linear_priority": issue.get("priorityLabel", ""),
            
            # Project metadata (from JSON or title)
            "project_code": metadata.get("project_code", "") if metadata else "",
            "project_name_th": title_data.get("name", issue["title"]),
            "project_name_en": "",  # Optional
            "fiscal_year": metadata.get("start_date", "")[:4] if metadata and metadata.get("start_date") else title_data.get("year", "2569"),
            
            # Type & Classification
            "type": metadata.get("type", "") if metadata else title_data.get("type", ""),
            "region": metadata.get("region", "") if metadata else title_data.get("region", ""),
            "status": metadata.get("status", "active") if metadata else "active",
            
            # Budget
            "budget": metadata.get("budget", 0) if metadata else 0,
            "budget_scale": metadata.get("budget_scale", "") if metadata else "",
            
            # Timeline
            "start_date": metadata.get("start_date", "") if metadata else "",
            "end_date": metadata.get("end_date", "") if metadata else issue.get("dueDate", ""),
            "duration_months": metadata.get("duration_months", 0) if metadata else 0,
            
            # Ownership
            "owner": metadata.get("owner", "") if metadata else "",
            "lead_agency": metadata.get("lead_agency", "NIEMS") if metadata else "NIEMS",
            "assignee": issue["assignee"]["email"] if issue.get("assignee") else "",
            
            # Progress
            "progress_percentage": metadata.get("progress_percentage", 0) if metadata else 0,
            
            # Timestamps
            "created_at": issue["createdAt"],
            "updated_at": issue["updatedAt"],
            "last_synced": datetime.now().isoformat()
        }
        
        return row
    
    def export_to_csv(self, output_path: str = "data/projects_master_2569.csv"):
        """Export Linear issues to CSV file"""
        
        # Fetch issues
        issues = self.fetch_issues()
        
        if not issues:
            print("⚠️  No issues found")
            return
        
        # Convert to CSV rows
        rows = [self.convert_to_csv_row(issue) for issue in issues]
        
        # Get fieldnames from first row
        fieldnames = list(rows[0].keys())
        
        # Write to CSV
        try:
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            
            print(f"✅ Exported {len(rows)} projects to {output_path}")
            print(f"📊 Columns: {len(fieldnames)}")
            
        except IOError as e:
            print(f"❌ Error writing CSV: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Export NIEMS Project issues from Linear to CSV"
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("LINEAR_API_KEY"),
        help="Linear API key (or set LINEAR_API_KEY env var)"
    )
    parser.add_argument(
        "--team",
        default=os.getenv("LINEAR_TEAM_ID", "STR"),
        help="Linear team ID (default: STR)"
    )
    parser.add_argument(
        "--output",
        default="data/projects_master_2569.csv",
        help="Output CSV file path"
    )
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("❌ Error: LINEAR_API_KEY is required")
        print("   Set via --api-key or LINEAR_API_KEY environment variable")
        sys.exit(1)
    
    # Export
    exporter = LinearExporter(args.api_key, args.team)
    exporter.export_to_csv(args.output)
    
    print("\n✨ Export complete!")


if __name__ == "__main__":
    main()

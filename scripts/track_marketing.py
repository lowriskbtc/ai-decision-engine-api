"""
Marketing Progress Tracker
Tracks marketing efforts and measures reach
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class MarketingTracker:
    """Track marketing campaigns and progress"""
    
    def __init__(self):
        self.tracker_file = "marketing_progress.json"
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create tracker file if it doesn't exist"""
        if not Path(self.tracker_file).exists():
            initial_data = {
                "created_at": datetime.now().isoformat(),
                "overall_metrics": {
                    "total_visitors": 0,
                    "total_signups": 0,
                    "total_api_calls": 0,
                    "paying_customers": 0,
                    "revenue": 0
                },
                "platforms": {
                    "reddit": [],
                    "hackernews": [],
                    "twitter": [],
                    "producthunt": [],
                    "indiehackers": [],
                    "devto": [],
                    "linkedin": []
                },
                "daily_updates": [],
                "goals": {
                    "week1": {"visitors": 500, "signups": 50},
                    "week2": {"visitors": 1000, "signups": 100, "paying": 5},
                    "month1": {"visitors": 5000, "signups": 500, "paying": 20, "revenue": 180}
                }
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load tracker data"""
        try:
            with open(self.tracker_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self, data: Dict[str, Any]):
        """Save tracker data"""
        with open(self.tracker_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def record_post(self, platform: str, post_type: str, url: str = "", notes: str = ""):
        """Record a marketing post"""
        data = self._load_data()
        
        post_record = {
            "date": datetime.now().isoformat(),
            "platform": platform,
            "post_type": post_type,
            "url": url,
            "notes": notes,
            "visitors": 0,
            "signups": 0,
            "api_calls": 0,
            "engagement": 0,
            "status": "posted"
        }
        
        if platform not in data.get("platforms", {}):
            data["platforms"][platform] = []
        
        data["platforms"][platform].append(post_record)
        self._save_data(data)
        
        print(f"✅ Recorded {post_type} post on {platform}")
        return post_record
    
    def update_post_metrics(self, platform: str, post_index: int, visitors: int = None, 
                           signups: int = None, api_calls: int = None, engagement: int = None):
        """Update metrics for a specific post"""
        data = self._load_data()
        
        if platform in data.get("platforms", {}):
            posts = data["platforms"][platform]
            if 0 <= post_index < len(posts):
                post = posts[post_index]
                if visitors is not None:
                    post["visitors"] = visitors
                if signups is not None:
                    post["signups"] = signups
                if api_calls is not None:
                    post["api_calls"] = api_calls
                if engagement is not None:
                    post["engagement"] = engagement
                
                # Update overall metrics
                self._update_overall_metrics(data)
                self._save_data(data)
                
                print(f"✅ Updated metrics for {platform} post #{post_index}")
                return True
        
        print(f"❌ Could not find post to update")
        return False
    
    def _update_overall_metrics(self, data: Dict[str, Any]):
        """Update overall metrics from all posts"""
        total_visitors = 0
        total_signups = 0
        total_api_calls = 0
        
        for platform, posts in data.get("platforms", {}).items():
            for post in posts:
                total_visitors += post.get("visitors", 0)
                total_signups += post.get("signups", 0)
                total_api_calls += post.get("api_calls", 0)
        
        data["overall_metrics"] = {
            "total_visitors": total_visitors,
            "total_signups": total_signups,
            "total_api_calls": total_api_calls,
            "paying_customers": data.get("overall_metrics", {}).get("paying_customers", 0),
            "revenue": data.get("overall_metrics", {}).get("revenue", 0),
            "last_updated": datetime.now().isoformat()
        }
    
    def add_daily_update(self, date: str, actions: List[str], visitors: int = 0, 
                        signups: int = 0, api_calls: int = 0, notes: str = ""):
        """Add a daily update"""
        data = self._load_data()
        
        update = {
            "date": date,
            "actions": actions,
            "visitors": visitors,
            "signups": signups,
            "api_calls": api_calls,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        
        if "daily_updates" not in data:
            data["daily_updates"] = []
        
        data["daily_updates"].append(update)
        self._save_data(data)
        
        print(f"✅ Added daily update for {date}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all marketing efforts"""
        data = self._load_data()
        
        summary = {
            "overall": data.get("overall_metrics", {}),
            "by_platform": {},
            "top_performers": []
        }
        
        # Calculate by platform
        for platform, posts in data.get("platforms", {}).items():
            platform_total = {
                "posts": len(posts),
                "visitors": sum(p.get("visitors", 0) for p in posts),
                "signups": sum(p.get("signups", 0) for p in posts),
                "api_calls": sum(p.get("api_calls", 0) for p in posts)
            }
            summary["by_platform"][platform] = platform_total
        
        # Find top performing posts
        all_posts = []
        for platform, posts in data.get("platforms", {}).items():
            for post in posts:
                all_posts.append({
                    "platform": platform,
                    "post_type": post.get("post_type", ""),
                    "visitors": post.get("visitors", 0),
                    "signups": post.get("signups", 0)
                })
        
        summary["top_performers"] = sorted(
            all_posts, 
            key=lambda x: x["visitors"], 
            reverse=True
        )[:5]
        
        return summary
    
    def print_summary(self):
        """Print a formatted summary"""
        summary = self.get_summary()
        
        print("\n" + "="*50)
        print("📊 MARKETING PROGRESS SUMMARY")
        print("="*50)
        
        print("\n🎯 Overall Metrics:")
        overall = summary["overall"]
        print(f"  Total Visitors: {overall.get('total_visitors', 0):,}")
        print(f"  Total Signups: {overall.get('total_signups', 0):,}")
        print(f"  Total API Calls: {overall.get('total_api_calls', 0):,}")
        print(f"  Paying Customers: {overall.get('paying_customers', 0)}")
        print(f"  Revenue: ${overall.get('revenue', 0):.2f}")
        
        print("\n📈 By Platform:")
        for platform, metrics in summary["by_platform"].items():
            if metrics["posts"] > 0:
                print(f"  {platform.upper()}:")
                print(f"    Posts: {metrics['posts']}")
                print(f"    Visitors: {metrics['visitors']:,}")
                print(f"    Signups: {metrics['signups']:,}")
                print(f"    API Calls: {metrics['api_calls']:,}")
        
        if summary["top_performers"]:
            print("\n🏆 Top Performing Posts:")
            for i, post in enumerate(summary["top_performers"], 1):
                print(f"  {i}. {post['platform']} - {post['post_type']}")
                print(f"     Visitors: {post['visitors']:,}, Signups: {post['signups']:,}")
        
        print("\n" + "="*50 + "\n")


# Global instance
marketing_tracker = MarketingTracker()

if __name__ == "__main__":
    # Example usage
    tracker = MarketingTracker()
    
    # Record a post
    tracker.record_post("reddit", "r/SideProject launch", 
                       notes="First marketing post")
    
    # Update metrics
    tracker.update_post_metrics("reddit", 0, visitors=150, signups=12)
    
    # Print summary
    tracker.print_summary()


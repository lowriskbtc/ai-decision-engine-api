"""
AI-Driven Tweet System - Status
Run this to see current status and get next tweet
"""

from autonomous_tweet_scheduler import AutonomousTweetScheduler
from datetime import datetime
import os

def main():
    print("=" * 60)
    print("AI WEED COMPANY - AUTONOMOUS TWEET SYSTEM")
    print("=" * 60)
    print(f"Status: ACTIVE")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    scheduler = AutonomousTweetScheduler()
    
    # Generate next tweet
    tweet = scheduler.get_next_tweet()
    
    # Display tweet
    print("NEXT TWEET (AI SELECTED):")
    print("-" * 60)
    print(tweet)
    print("-" * 60)
    print(f"Character count: {len(tweet)}")
    print()
    
    # Show metrics
    print("CURRENT METRICS:")
    print(f"  Revenue: ${scheduler.metrics['revenue']:,.2f}")
    print(f"  Active Strategies: {scheduler.metrics['strategies_active']}")
    print(f"  Decisions Made: {scheduler.metrics['decisions_made']}")
    print(f"  Current Phase: {scheduler.metrics['phase']}")
    print()
    
    # Check if files exist
    if os.path.exists("next_tweet.txt"):
        print("✅ Tweet saved to: next_tweet.txt")
    if os.path.exists("tweet_schedule.json"):
        print("✅ Schedule saved to: tweet_schedule.json")
    if os.path.exists("tweet_history.json"):
        print("✅ History saved to: tweet_history.json")
    
    print()
    print("=" * 60)
    print("AI operates autonomously. Copy tweet from next_tweet.txt to post.")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()


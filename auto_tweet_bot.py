"""
Auto-posting system that runs continuously
AI selects and prepares tweets autonomously
"""

import schedule
import time
from autonomous_tweet_scheduler import AutonomousTweetScheduler
from datetime import datetime

class AutoTweetBot:
    """Fully autonomous tweet bot"""
    
    def __init__(self):
        self.scheduler = AutonomousTweetScheduler()
        self.setup_schedule()
    
    def setup_schedule(self):
        """AI sets up posting schedule"""
        # Morning post: 9-11 AM
        schedule.every().day.at("10:00").do(self.post_tweet)
        
        # Afternoon post: 1-3 PM  
        schedule.every().day.at("14:00").do(self.post_tweet)
        
        # Evening post: 7-9 PM
        schedule.every().day.at("20:00").do(self.post_tweet)
    
    def post_tweet(self):
        """AI selects and prepares tweet"""
        tweet = self.scheduler.get_next_tweet()
        
        # Save for posting
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tweet_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(tweet)
        
        print(f"[{datetime.now()}] AI selected tweet saved to {filename}")
        print(f"Tweet: {tweet[:100]}...")
        
        return tweet
    
    def run(self):
        """Run continuously"""
        print("=" * 60)
        print("AUTONOMOUS TWEET BOT - RUNNING")
        print("=" * 60)
        print("AI will select tweets at:")
        print("  • 10:00 AM (Morning)")
        print("  • 2:00 PM (Afternoon)")
        print("  • 8:00 PM (Evening)")
        print("\nTweets saved to: tweet_YYYYMMDD_HHMMSS.txt")
        print("=" * 60)
        print("\nRunning... Press Ctrl+C to stop\n")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    bot = AutoTweetBot()
    
    # Generate immediate tweet
    immediate_tweet = bot.post_tweet()
    
    # Run continuous schedule
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n\nBot stopped.")


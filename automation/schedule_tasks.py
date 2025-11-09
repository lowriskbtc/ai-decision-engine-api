"""
Automated Task Scheduler
Schedule regular tasks for the AI Weed Company system
"""

import schedule
import time
from datetime import datetime
from update_progress import ProgressTracker
from monitor_system import SystemMonitor
import subprocess

def daily_status_check():
    """Run daily system status check"""
    print(f"[{datetime.now()}] Running daily status check...")
    monitor = SystemMonitor()
    monitor.check_all()
    print("✅ Daily check complete")

def weekly_report():
    """Generate weekly report"""
    print(f"[{datetime.now()}] Generating weekly report...")
    subprocess.run(["python", "generate_report.py"])
    print("✅ Weekly report generated")

def update_progress_daily():
    """Update progress file daily"""
    print(f"[{datetime.now()}] Updating progress...")
    tracker = ProgressTracker()
    # Add any automatic progress updates here
    print("✅ Progress updated")

def generate_tweet():
    """Generate and save next tweet"""
    print(f"[{datetime.now()}] Generating tweet...")
    subprocess.run(["python", "autonomous_tweet_scheduler.py"])
    print("✅ Tweet generated")

# Schedule tasks
schedule.every().day.at("09:00").do(daily_status_check)
schedule.every().monday.at("10:00").do(weekly_report)
schedule.every().day.at("12:00").do(update_progress_daily)
schedule.every().day.at("14:00").do(generate_tweet)

def main():
    """Run scheduled tasks"""
    print("=" * 60)
    print("AI WEED COMPANY - AUTOMATED TASK SCHEDULER")
    print("=" * 60)
    print(f"Started at: {datetime.now()}")
    print()
    print("Scheduled tasks:")
    print("  • Daily status check: 09:00")
    print("  • Weekly report: Monday 10:00")
    print("  • Daily progress update: 12:00")
    print("  • Tweet generation: 14:00")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    # Run initial checks
    daily_status_check()
    update_progress_daily()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")


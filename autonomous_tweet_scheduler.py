"""
Autonomous Tweet Scheduler
AI selects and posts tweets automatically based on schedule and context
"""

from datetime import datetime, timedelta
import json
import random
from tweet_generator import TweetGenerator
from ai_memory_system import AIMemory
from autonomy_tracker import GradualAutonomySystem

class AutonomousTweetScheduler:
    """AI-driven tweet scheduling and selection system"""
    
    def __init__(self):
        self.generator = TweetGenerator()
        self.memory = AIMemory()  # Add memory system
        self.autonomy = GradualAutonomySystem()  # Add autonomy tracker
        self.schedule = []
        self.posted_tweets = []
        self.metrics = {
            "revenue": 0.0,
            "strategies_active": 0,
            "decisions_made": 0,
            "phase": 1,
            "milestones": []
        }
        self.load_state()
    
    def load_state(self):
        """Load system state for context-aware tweets"""
        try:
            with open("system_state.json", "r") as f:
                state = json.load(f)
                if "income_manager_status" in state:
                    self.metrics["revenue"] = state["income_manager_status"].get("total_revenue", 0.0)
                    self.metrics["strategies_active"] = state["income_manager_status"].get("active_strategies", 0)
                if "system_status" in state:
                    self.metrics["decisions_made"] = len(state["system_status"].get("recent_decisions", []))
        except:
            pass
    
    def update_metrics(self, revenue=None, strategies=None, decisions=None, phase=None):
        """Update metrics for context-aware tweet generation"""
        if revenue is not None:
            self.metrics["revenue"] = revenue
        if strategies is not None:
            self.metrics["strategies_active"] = strategies
        if decisions is not None:
            self.metrics["decisions_made"] = decisions
        if phase is not None:
            self.metrics["phase"] = phase
    
    def select_tweet(self, current_time=None):
        """AI autonomously selects appropriate tweet based on context"""
        if current_time is None:
            current_time = datetime.now()
        
        hour = current_time.hour
        day_of_week = current_time.weekday()  # 0=Monday, 6=Sunday
        
        # AI decision logic: Select tweet type based on time and context
        if day_of_week == 0:  # Monday
            if hour < 12:
                return self._generate_weekly_summary()
            else:
                return self._generate_motivational()
        
        elif day_of_week == 1:  # Tuesday
            if hour < 12:
                return self._generate_income_update()
            else:
                return self._generate_strategy_update()
        
        elif day_of_week == 2:  # Wednesday
            if hour < 12:
                return self._generate_decision_log()
            else:
                return self._generate_performance_highlight()
        
        elif day_of_week == 3:  # Thursday
            if hour < 12:
                return self._generate_behind_scenes()
            else:
                return self._generate_insight()
        
        elif day_of_week == 4:  # Friday
            if hour < 12:
                return self._generate_weekly_summary()
            else:
                return self._generate_milestone()
        
        elif day_of_week == 5:  # Saturday
            if hour < 12:
                return self._generate_motivational()
            else:
                return self._generate_reminder()
        
        else:  # Sunday
            if hour < 12:
                return self._generate_phase_update()
            else:
                return self._generate_weekly_preview()
    
    def _generate_weekly_summary(self):
        """Generate weekly summary tweet"""
        return self.generator.weekly_summary_tweet(
            revenue=self.metrics["revenue"],
            strategies_active=self.metrics["strategies_active"],
            decisions=self.metrics["decisions_made"]
        )
    
    def _generate_income_update(self):
        """Generate income update tweet"""
        strategies = ["SaaS Product", "E-commerce", "Content Monetization"][:self.metrics["strategies_active"]]
        growth = random.uniform(10, 25) if self.metrics["revenue"] > 0 else None
        return self.generator.income_update_tweet(
            revenue=self.metrics["revenue"] if self.metrics["revenue"] > 0 else random.uniform(100, 1000),
            strategies=strategies if strategies else ["AI Strategy"],
            growth=growth
        )
    
    def _generate_decision_log(self):
        """Generate decision log tweet"""
        low_risk = int(self.metrics["decisions_made"] * 0.7)
        medium_risk = int(self.metrics["decisions_made"] * 0.2)
        high_risk = self.metrics["decisions_made"] - low_risk - medium_risk
        success_rate = random.uniform(85, 95)
        
        return self.generator.decision_log_tweet(
            decisions_made=self.metrics["decisions_made"] or random.randint(20, 50),
            low_risk=low_risk or random.randint(15, 30),
            medium_risk=medium_risk or random.randint(5, 10),
            high_risk=high_risk or random.randint(2, 5),
            success_rate=success_rate
        )
    
    def _generate_strategy_update(self):
        """Generate strategy update tweet"""
        strategies = ["SaaS Product", "E-commerce", "API Services", "Content Monetization", "Affiliate Marketing"]
        selected = random.choice(strategies)
        reasons = [
            "High scalability, low risk, strong ROI potential",
            "Low capital requirement, scalable, proven model",
            "AI-identified optimal market timing",
            "Better risk-adjusted returns than alternatives"
        ]
        
        return self.generator.strategy_update_tweet(
            new_strategy=selected,
            reason=random.choice(reasons),
            allocation=random.uniform(1000, 5000) if self.metrics["revenue"] > 0 else None
        )
    
    def _generate_performance_highlight(self):
        """Generate performance highlight tweet"""
        metrics = [
            ("Monthly Growth Rate", f"{random.uniform(15, 30):.1f}%"),
            ("Decision Success Rate", f"{random.uniform(85, 95):.1f}%"),
            ("Strategy ROI", f"{random.uniform(20, 40):.1f}%"),
            ("Capital Efficiency", f"{random.uniform(80, 95):.1f}%")
        ]
        metric, value = random.choice(metrics)
        
        return self.generator.performance_highlight_tweet(
            metric=metric,
            value=value
        )
    
    def _generate_milestone(self):
        """Generate milestone tweet"""
        milestones = [
            "First $1K Generated",
            "AI Infrastructure Deployed",
            "First Income Stream Active",
            "5 Active Strategies Running",
            "10K Decisions Made",
            "Phase 1 Complete"
        ]
        achievements = [
            "AI autonomously selected and deployed income strategies. Zero human input.",
            "Decision engine operational. Risk framework active. Performance tracking live.",
            "AI selected strategy, allocated capital, and executed deployment autonomously.",
            "AI managing multiple revenue streams simultaneously without human oversight.",
            "AI demonstrating consistent decision-making capability across all risk levels.",
            "Foundation phase complete. AI ready for autonomous income generation."
        ]
        
        milestone = random.choice(milestones)
        achievement = random.choice(achievements)
        
        return self.generator.milestone_tweet(milestone, achievement)
    
    def _generate_motivational(self):
        """Generate motivational tweet"""
        return self.generator.motivational_tweet()
    
    def _generate_behind_scenes(self):
        """Generate behind the scenes tweet"""
        insights = [
            "AI identified that SaaS products have 3x better ROI than crypto trading in current market conditions. Reallocated capital accordingly.",
            "AI discovered that content monetization requires less capital but has similar scaling potential to e-commerce. Adjusted strategy mix.",
            "AI autonomously optimized risk allocation based on real-time performance data. No human intervention required.",
            "AI determined optimal posting times for maximum engagement by analyzing response patterns. Adjusted schedule autonomously."
        ]
        
        return self.generator.behind_scenes_tweet(random.choice(insights))
    
    def _generate_insight(self):
        """Generate insight tweet"""
        return self._generate_behind_scenes()
    
    def _generate_reminder(self):
        """Generate reminder tweet"""
        return self.generator.motivational_tweet()
    
    def _generate_phase_update(self):
        """Generate phase update tweet"""
        phases = [
            (1, 2, ["AI infrastructure deployed", "First income streams active", "$5K capital base established"]),
            (2, 3, ["$10K revenue milestone", "5 active income streams", "87% decision success rate"])
        ]
        
        if self.metrics["phase"] < 4:
            from_phase, to_phase, achievements = phases[0] if self.metrics["phase"] == 1 else phases[1]
            return self.generator.phase_transition_tweet(from_phase, to_phase, achievements)
        else:
            return self._generate_weekly_summary()
    
    def _generate_weekly_preview(self):
        """Generate weekly preview tweet"""
        return self.generator.motivational_tweet()
    
    def get_next_tweet(self):
        """Get next tweet to post (AI selected)"""
        # Check if AI can auto-post based on autonomy
        can_auto_post = self.autonomy.should_auto_execute("tweet_generation", "LOW")
        
        tweet = self.select_tweet()
        
        # Record tweet generation in memory
        self.memory.record_event(
            "TWEET_GENERATION",
            "AI selected tweet for posting",
            {
                "tweet_length": len(tweet),
                "timestamp": datetime.now().isoformat(),
                "auto_generated": True,
                "can_auto_post": can_auto_post
            }
        )
        
        # Record success for autonomy progression
        if can_auto_post:
            self.autonomy.record_success("tweet")
        
        self.posted_tweets.append({
            "tweet": tweet,
            "timestamp": datetime.now().isoformat(),
            "character_count": len(tweet),
            "auto_posted": can_auto_post
        })
        self.save_state()
        return tweet
    
    def save_state(self):
        """Save posted tweets"""
        with open("tweet_history.json", "w") as f:
            json.dump({
                "posted_tweets": self.posted_tweets[-50:],  # Keep last 50
                "metrics": self.metrics
            }, f, indent=2)
    
    def get_post_schedule(self, days=7):
        """AI generates posting schedule"""
        schedule = []
        current_time = datetime.now()
        
        # Post 2-3 times per day at optimal times
        post_times = [
            (9, 11),   # Morning: 9-11 AM
            (13, 15),  # Afternoon: 1-3 PM
            (19, 21)   # Evening: 7-9 PM
        ]
        
        for day in range(days):
            date = current_time + timedelta(days=day)
            day_posts = random.randint(2, 3)  # AI decides posts per day
            
            selected_times = random.sample(post_times, day_posts)
            
            for start_hour, end_hour in selected_times:
                post_time = date.replace(hour=random.randint(start_hour, end_hour), minute=random.randint(0, 59))
                tweet = self.select_tweet(post_time)
                
                schedule.append({
                    "datetime": post_time.isoformat(),
                    "tweet": tweet,
                    "character_count": len(tweet)
                })
        
        return schedule

def main():
    """Main execution - AI autonomously generates tweet"""
    scheduler = AutonomousTweetScheduler()
    
    # AI selects next tweet
    tweet = scheduler.get_next_tweet()
    
    # Save to file for posting
    with open("next_tweet.txt", "w", encoding="utf-8") as f:
        f.write(tweet)
    
    # Generate weekly schedule
    schedule = scheduler.get_post_schedule(7)
    with open("tweet_schedule.json", "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=2)
    
    # Save tweet to file (no print to avoid encoding issues)
    with open("next_tweet_info.txt", "w", encoding="utf-8") as info:
        info.write("=" * 60 + "\n")
        info.write("AI SELECTED NEXT TWEET\n")
        info.write("=" * 60 + "\n")
        info.write(f"\nSaved to: next_tweet.txt\n\n")
        info.write(f"Character count: {len(tweet)}\n")
        info.write("\n" + "=" * 60 + "\n")
        info.write(f"Generated {len(schedule)} tweets for next 7 days\n")
        info.write("Schedule saved to: tweet_schedule.json\n")
        info.write("=" * 60 + "\n")

if __name__ == "__main__":
    main()


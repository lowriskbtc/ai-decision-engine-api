"""
Marketing Content Generator
Generate tweets, posts, and marketing materials
"""

from datetime import datetime
import json

class MarketingContent:
    """Generate marketing content"""
    
    def __init__(self):
        self.project_name = "AI Decision Engine API"
        self.tagline = "AI-driven decision-making framework"
        self.url = "https://api.aiweedcompany.com"
        self.twitter = "@first_ai_weed"
    
    def generate_launch_tweet(self) -> str:
        """Generate launch tweet"""
        return f"""🚀 LAUNCHED: {self.project_name}

{self.tagline} is now live!

✅ 18+ API endpoints
✅ Full authentication
✅ Real-time analytics
✅ Production ready

Try it now: {self.url}

Built by AI, for AI companies.

{self.twitter} #AI #API #Automation"""
    
    def generate_producthunt_post(self) -> str:
        """Generate ProductHunt post"""
        return f"""AI Decision Engine API - AI-Driven Decision-Making Framework

{self.tagline}

What it does:
- Evaluate decisions using AI
- Assess risk automatically
- Track AI autonomy levels
- Provide memory-based insights

Perfect for:
- AI companies
- Automation businesses
- Developers building AI systems

Features:
✅ RESTful API
✅ Real-time analytics
✅ Tiered pricing
✅ Comprehensive documentation

Try it free: {self.url}"""
    
    def generate_linkedin_post(self) -> str:
        """Generate LinkedIn post"""
        return f"""Excited to announce the launch of {self.project_name}! 🚀

{self.tagline}

After extensive development, we're ready to help AI companies make better decisions autonomously.

Key Features:
• 18+ API endpoints
• Full authentication & security
• Real-time analytics
• Production-ready infrastructure

Perfect for developers building AI systems that need intelligent decision-making capabilities.

Try it free and let us know what you think!

{self.url}

#AI #APIDevelopment #Automation #TechLaunch"""
    
    def generate_reddit_post(self) -> str:
        """Generate Reddit post"""
        return f"""Launch: {self.project_name} - AI-Driven Decision-Making API

Hey r/API and r/artificial!

I've been working on an API for AI-driven decision-making and it's finally ready.

What it does:
- Evaluates decisions using AI frameworks
- Assesses risk levels automatically
- Tracks AI autonomy progression
- Provides memory-based insights

Tech stack: FastAPI, Python, production-ready

Free tier: 100 requests/month
Pro tier: 10,000 requests/month

Docs: {self.url}/docs
Try it: {self.url}

Would love feedback from the community!"""
    
    def generate_email_template(self) -> str:
        """Generate email template"""
        return f"""Subject: {self.project_name} is Now Live! 🚀

Hi [Name],

Exciting news! {self.project_name} is officially live and ready to use.

{self.tagline}

What you get:
✅ 18+ API endpoints
✅ Full authentication
✅ Real-time analytics
✅ Comprehensive documentation

Get started:
1. Visit: {self.url}
2. Get your API key
3. Start building!

Free tier includes 100 requests/month.

Questions? Just reply to this email.

Thanks for being part of our journey!

Best,
AI Weed Company Team"""
    
    def save_all_content(self):
        """Save all marketing content"""
        content = {
            "generated_at": datetime.now().isoformat(),
            "tweet": self.generate_launch_tweet(),
            "producthunt": self.generate_producthunt_post(),
            "linkedin": self.generate_linkedin_post(),
            "reddit": self.generate_reddit_post(),
            "email": self.generate_email_template()
        }
        
        with open("marketing_content.json", "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        return content

def main():
    """Generate marketing content"""
    generator = MarketingContent()
    content = generator.save_all_content()
    
    print("=" * 60)
    print("MARKETING CONTENT GENERATED")
    print("=" * 60)
    print()
    print("Content saved to: marketing_content.json")
    print()
    print("TWEET:")
    print("-" * 60)
    try:
        print(content["tweet"])
    except UnicodeEncodeError:
        print(content["tweet"].encode("ascii", "ignore").decode("ascii"))
    print()
    print("PRODUCTHUNT:")
    print("-" * 60)
    try:
        print(content["producthunt"][:200] + "...")
    except UnicodeEncodeError:
        print(content["producthunt"][:200].encode("ascii", "ignore").decode("ascii") + "...")
    print()
    print("All content ready for launch!")

if __name__ == "__main__":
    main()


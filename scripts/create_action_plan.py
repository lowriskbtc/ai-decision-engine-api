"""
Action Plan Generator
Create daily action plan to get first customers
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

def create_action_plan():
    """Create 30-day action plan"""
    
    plan = {
        "created_at": datetime.now().isoformat(),
        "goal": "Get first paying customer in 30 days",
        "budget": 0,
        "daily_actions": {}
    }
    
    # Week 1: Launch & Get Users
    for day in range(1, 8):
        date = (datetime.now() + timedelta(days=day-1)).strftime("%Y-%m-%d")
        if day == 1:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "Deploy & Launch",
                "tasks": [
                    "Deploy to Railway (free)",
                    "Verify deployment works",
                    "Post on r/API (Reddit)",
                    "Share on Twitter/X",
                    "Post on HackerNews (Show HN)",
                    "Get first 5 users"
                ],
                "goal": "Get API live and first users"
            }
        elif day == 2:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "Marketing Push",
                "tasks": [
                    "Post on r/startups",
                    "Post on r/SideProject",
                    "Engage with Reddit comments",
                    "Share on LinkedIn",
                    "Respond to HN comments",
                    "Get 5 more users"
                ],
                "goal": "Build visibility"
            }
        elif day == 3:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "Content Creation",
                "tasks": [
                    "Write blog post (Dev.to)",
                    "Create demo video (optional)",
                    "Update documentation",
                    "Create case study template",
                    "Engage with users"
                ],
                "goal": "Create content assets"
            }
        elif day == 4:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "ProductHunt Launch",
                "tasks": [
                    "Prepare ProductHunt listing",
                    "Schedule launch (if possible)",
                    "Reach out to potential upvoters",
                    "Create launch assets",
                    "Prepare launch day content"
                ],
                "goal": "Prepare for ProductHunt"
            }
        elif day == 5:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "User Engagement",
                "tasks": [
                    "Respond to all comments",
                    "Help users integrate",
                    "Collect feedback",
                    "Fix any issues",
                    "Engage on social media"
                ],
                "goal": "Build relationships"
            }
        elif day == 6:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "Outreach",
                "tasks": [
                    "Find potential users",
                    "Reach out directly (email/Twitter)",
                    "Offer free API keys",
                    "Ask for feedback",
                    "Build email list"
                ],
                "goal": "Direct user acquisition"
            }
        else:  # day 7
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "Week 1 Review",
                "tasks": [
                    "Review week 1 metrics",
                    "Count total users",
                    "Analyze what worked",
                    "Plan week 2",
                    "Prepare Stripe integration"
                ],
                "goal": "Review and plan"
            }
    
    # Week 2: Add Payments & Convert
    for day in range(8, 15):
        date = (datetime.now() + timedelta(days=day-1)).strftime("%Y-%m-%d")
        if day == 8:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "Stripe Integration",
                "tasks": [
                    "Sign up for Stripe (free)",
                    "Add Stripe to API",
                    "Create payment endpoints",
                    "Test payment flow",
                    "Update pricing page"
                ],
                "goal": "Enable payments"
            }
        elif day == 9:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "Launch Paid Tiers",
                "tasks": [
                    "Activate Pro tier ($9/month)",
                    "Update documentation",
                    "Email free users about upgrade",
                    "Create upgrade flow",
                    "Test payment process"
                ],
                "goal": "Launch paid plans"
            }
        elif day == 10:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "Conversion Push",
                "tasks": [
                    "Reach out to high-usage free users",
                    "Offer upgrade incentives",
                    "Create upgrade messaging",
                    "A/B test pricing",
                    "Track conversions"
                ],
                "goal": "Convert free to paid"
            }
        else:
            plan["daily_actions"][date] = {
                "day": f"Day {day}",
                "focus": "Continue Marketing",
                "tasks": [
                    "Post on social media",
                    "Engage with community",
                    "Help users",
                    "Collect feedback",
                    "Iterate on product"
                ],
                "goal": "Maintain momentum"
            }
    
    # Week 3-4: Scale
    for day in range(15, 31):
        date = (datetime.now() + timedelta(days=day-1)).strftime("%Y-%m-%d")
        plan["daily_actions"][date] = {
            "day": f"Day {day}",
            "focus": "Scale & Optimize",
            "tasks": [
                "Continue marketing",
                "Convert users",
                "Improve product",
                "Build features",
                "Get first paying customer!"
            ],
            "goal": "First paying customer"
        }
    
    # Save JSON
    with open("30_DAY_ACTION_PLAN.json", "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    
    # Create markdown
    md_content = """# 30-Day Action Plan - Get First Paying Customer

## Goal: First Paying Customer in 30 Days
## Budget: $0

---

## Week 1: Launch & Get Users

### Day 1: Deploy & Launch
- [ ] Deploy to Railway (free)
- [ ] Verify deployment works
- [ ] Post on r/API (Reddit)
- [ ] Share on Twitter/X
- [ ] Post on HackerNews (Show HN)
- [ ] Get first 5 users

**Goal:** Get API live and first users

### Day 2: Marketing Push
- [ ] Post on r/startups
- [ ] Post on r/SideProject
- [ ] Engage with Reddit comments
- [ ] Share on LinkedIn
- [ ] Respond to HN comments
- [ ] Get 5 more users

**Goal:** Build visibility

### Day 3: Content Creation
- [ ] Write blog post (Dev.to)
- [ ] Create demo video (optional)
- [ ] Update documentation
- [ ] Create case study template
- [ ] Engage with users

**Goal:** Create content assets

### Day 4: ProductHunt Prep
- [ ] Prepare ProductHunt listing
- [ ] Schedule launch (if possible)
- [ ] Reach out to potential upvoters
- [ ] Create launch assets
- [ ] Prepare launch day content

**Goal:** Prepare for ProductHunt

### Day 5: User Engagement
- [ ] Respond to all comments
- [ ] Help users integrate
- [ ] Collect feedback
- [ ] Fix any issues
- [ ] Engage on social media

**Goal:** Build relationships

### Day 6: Outreach
- [ ] Find potential users
- [ ] Reach out directly (email/Twitter)
- [ ] Offer free API keys
- [ ] Ask for feedback
- [ ] Build email list

**Goal:** Direct user acquisition

### Day 7: Week 1 Review
- [ ] Review week 1 metrics
- [ ] Count total users
- [ ] Analyze what worked
- [ ] Plan week 2
- [ ] Prepare Stripe integration

**Goal:** Review and plan

---

## Week 2: Add Payments & Convert

### Day 8: Stripe Integration
- [ ] Sign up for Stripe (free)
- [ ] Add Stripe to API
- [ ] Create payment endpoints
- [ ] Test payment flow
- [ ] Update pricing page

**Goal:** Enable payments

### Day 9: Launch Paid Tiers
- [ ] Activate Pro tier ($9/month)
- [ ] Update documentation
- [ ] Email free users about upgrade
- [ ] Create upgrade flow
- [ ] Test payment process

**Goal:** Launch paid plans

### Day 10: Conversion Push
- [ ] Reach out to high-usage free users
- [ ] Offer upgrade incentives
- [ ] Create upgrade messaging
- [ ] A/B test pricing
- [ ] Track conversions

**Goal:** Convert free to paid

### Days 11-14: Continue Marketing
- [ ] Post on social media
- [ ] Engage with community
- [ ] Help users
- [ ] Collect feedback
- [ ] Iterate on product

**Goal:** Maintain momentum

---

## Week 3-4: Scale

### Days 15-30: Scale & Optimize
- [ ] Continue marketing
- [ ] Convert users
- [ ] Improve product
- [ ] Build features
- [ ] **Get first paying customer!**

**Goal:** First paying customer

---

## Key Metrics to Track

- Total users
- Free users
- Paid users
- Revenue
- Conversion rate
- User feedback

---

## Success Criteria

✅ Week 1: 20+ free users
✅ Week 2: Payments enabled, first conversion attempt
✅ Week 3: First paying customer!
✅ Week 4: Multiple paying customers

---

*Stay focused, execute daily, iterate quickly!*

"""
    
    with open("30_DAY_ACTION_PLAN.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print("30-day action plan created:")
    print("  - 30_DAY_ACTION_PLAN.json")
    print("  - 30_DAY_ACTION_PLAN.md")
    print()
    print("Follow this daily to get your first paying customer!")

if __name__ == "__main__":
    create_action_plan()


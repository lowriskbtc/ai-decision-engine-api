"""
Autonomy Progression System
Gradually increases AI autonomy as it proves capable
Human maintains ownership with minimal operational input
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import json
from enum import Enum

class AutonomyLevel(Enum):
    """Autonomy levels"""
    LEVEL_1_HUMAN_LED = "LEVEL_1_HUMAN_LED"  # Current: Human makes most decisions
    LEVEL_2_AI_ASSISTED = "LEVEL_2_AI_ASSISTED"  # AI recommends, human approves
    LEVEL_3_AI_DRIVEN = "LEVEL_3_AI_DRIVEN"  # AI decides, human reviews high-risk
    LEVEL_4_HIGH_AUTONOMY = "LEVEL_4_HIGH_AUTONOMY"  # AI operates, human checks milestones
    LEVEL_5_FULL_AUTONOMY = "LEVEL_5_FULL_AUTONOMY"  # AI fully autonomous, human owns
    LEVEL_6_COMPLETE_AUTONOMY = "LEVEL_6_COMPLETE_AUTONOMY"  # AI runs everything, human interprets only

class AutonomyProgressionSystem:
    """Manages gradual transition to full AI autonomy"""
    
    def __init__(self, memory_file="autonomy_progression.json"):
        self.memory_file = memory_file
        self.progression = self.load_progression()
        self.current_level = AutonomyLevel(self.progression.get("current_level", "LEVEL_1_HUMAN_LED"))
        self.metrics = self.progression.get("metrics", {
            "total_decisions": 0,
            "ai_decisions": 0,
            "human_decisions": 0,
            "success_rate": 0.0,
            "human_interventions": 0,
            "autonomy_score": 0.0
        })
        self.milestones = self.progression.get("milestones", [])
    
    def load_progression(self) -> Dict[str, Any]:
        """Load progression state"""
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "current_level": "LEVEL_1_HUMAN_LED",
                "start_date": datetime.now().isoformat(),
                "metrics": {
                    "total_decisions": 0,
                    "ai_decisions": 0,
                    "human_decisions": 0,
                    "success_rate": 0.0,
                    "human_interventions": 0,
                    "autonomy_score": 0.0
                },
                "milestones": [],
                "transition_criteria": {}
            }
    
    def save_progression(self):
        """Save progression state"""
        self.progression["current_level"] = self.current_level.value
        self.progression["metrics"] = self.metrics
        self.progression["last_updated"] = datetime.now().isoformat()
        
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.progression, f, indent=2, ensure_ascii=False)
    
    def record_decision(self, decision_type: str, ai_made: bool, human_approved: bool, success: bool):
        """Record a decision to track autonomy progression"""
        self.metrics["total_decisions"] += 1
        
        if ai_made:
            self.metrics["ai_decisions"] += 1
        else:
            self.metrics["human_decisions"] += 1
        
        if not ai_made and human_approved:
            self.metrics["human_interventions"] += 1
        
        # Update success rate
        if self.metrics["total_decisions"] > 0:
            successful = self.metrics.get("successful_decisions", 0)
            if success:
                successful += 1
            self.metrics["successful_decisions"] = successful
            self.metrics["success_rate"] = (successful / self.metrics["total_decisions"]) * 100
        
        # Calculate autonomy score
        self._calculate_autonomy_score()
        
        # Check if ready for next level
        self._check_level_upgrade()
        
        self.save_progression()
    
    def _calculate_autonomy_score(self):
        """Calculate current autonomy score"""
        if self.metrics["total_decisions"] == 0:
            self.metrics["autonomy_score"] = 0.0
            return
        
        # Base score: percentage of AI decisions
        ai_decision_ratio = (self.metrics["ai_decisions"] / self.metrics["total_decisions"]) * 100
        
        # Success bonus: higher success rate = higher autonomy score
        success_bonus = (self.metrics["success_rate"] / 100) * 20
        
        # Intervention penalty: fewer interventions = higher score
        if self.metrics["total_decisions"] > 0:
            intervention_ratio = (self.metrics["human_interventions"] / self.metrics["total_decisions"]) * 100
            intervention_penalty = min(intervention_ratio * 2, 30)
        else:
            intervention_penalty = 0
        
        self.metrics["autonomy_score"] = ai_decision_ratio + success_bonus - intervention_penalty
        self.metrics["autonomy_score"] = max(0, min(100, self.metrics["autonomy_score"]))
    
    def _check_level_upgrade(self):
        """Check if ready to upgrade autonomy level"""
        current_score = self.metrics["autonomy_score"]
        success_rate = self.metrics["success_rate"]
        total_decisions = self.metrics["total_decisions"]
        
        # Level 1 -> Level 2: AI assisted
        if self.current_level == AutonomyLevel.LEVEL_1_HUMAN_LED:
            if total_decisions >= 20 and success_rate >= 70 and current_score >= 40:
                self.upgrade_level(AutonomyLevel.LEVEL_2_AI_ASSISTED)
        
        # Level 2 -> Level 3: AI driven
        elif self.current_level == AutonomyLevel.LEVEL_2_AI_ASSISTED:
            if total_decisions >= 50 and success_rate >= 80 and current_score >= 60:
                self.upgrade_level(AutonomyLevel.LEVEL_3_AI_DRIVEN)
        
        # Level 3 -> Level 4: High autonomy
        elif self.current_level == AutonomyLevel.LEVEL_3_AI_DRIVEN:
            if total_decisions >= 100 and success_rate >= 85 and current_score >= 75:
                self.upgrade_level(AutonomyLevel.LEVEL_4_HIGH_AUTONOMY)
        
        # Level 4 -> Level 5: Full autonomy
        elif self.current_level == AutonomyLevel.LEVEL_4_HIGH_AUTONOMY:
            if total_decisions >= 200 and success_rate >= 90 and current_score >= 85:
                self.upgrade_level(AutonomyLevel.LEVEL_5_FULL_AUTONOMY)
        
        # Level 5 -> Level 6: Complete autonomy
        elif self.current_level == AutonomyLevel.LEVEL_5_FULL_AUTONOMY:
            if total_decisions >= 500 and success_rate >= 92 and current_score >= 95:
                self.upgrade_level(AutonomyLevel.LEVEL_6_COMPLETE_AUTONOMY)
    
    def upgrade_level(self, new_level: AutonomyLevel):
        """Upgrade to new autonomy level"""
        old_level = self.current_level
        self.current_level = new_level
        
        milestone = {
            "id": f"MIL_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "from_level": old_level.value,
            "to_level": new_level.value,
            "autonomy_score": self.metrics["autonomy_score"],
            "success_rate": self.metrics["success_rate"],
            "total_decisions": self.metrics["total_decisions"]
        }
        
        self.milestones.append(milestone)
        self.progression["milestones"] = self.milestones
        
        self.save_progression()
        return milestone
    
    def get_autonomy_status(self) -> Dict[str, Any]:
        """Get current autonomy status"""
        return {
            "current_level": self.current_level.value,
            "autonomy_score": self.metrics["autonomy_score"],
            "success_rate": self.metrics["success_rate"],
            "total_decisions": self.metrics["total_decisions"],
            "ai_decisions": self.metrics["ai_decisions"],
            "human_decisions": self.metrics["human_decisions"],
            "human_interventions": self.metrics["human_interventions"],
            "ai_decision_percentage": (self.metrics["ai_decisions"] / max(1, self.metrics["total_decisions"])) * 100,
            "next_level_requirements": self._get_next_level_requirements()
        }
    
    def _get_next_level_requirements(self) -> Dict[str, Any]:
        """Get requirements for next level"""
        if self.current_level == AutonomyLevel.LEVEL_1_HUMAN_LED:
            return {
                "next_level": "LEVEL_2_AI_ASSISTED",
                "requirements": {
                    "total_decisions": 20,
                    "success_rate": 70,
                    "autonomy_score": 40
                },
                "current": {
                    "total_decisions": self.metrics["total_decisions"],
                    "success_rate": self.metrics["success_rate"],
                    "autonomy_score": self.metrics["autonomy_score"]
                }
            }
        elif self.current_level == AutonomyLevel.LEVEL_2_AI_ASSISTED:
            return {
                "next_level": "LEVEL_3_AI_DRIVEN",
                "requirements": {
                    "total_decisions": 50,
                    "success_rate": 80,
                    "autonomy_score": 60
                },
                "current": {
                    "total_decisions": self.metrics["total_decisions"],
                    "success_rate": self.metrics["success_rate"],
                    "autonomy_score": self.metrics["autonomy_score"]
                }
            }
        elif self.current_level == AutonomyLevel.LEVEL_3_AI_DRIVEN:
            return {
                "next_level": "LEVEL_4_HIGH_AUTONOMY",
                "requirements": {
                    "total_decisions": 100,
                    "success_rate": 85,
                    "autonomy_score": 75
                },
                "current": {
                    "total_decisions": self.metrics["total_decisions"],
                    "success_rate": self.metrics["success_rate"],
                    "autonomy_score": self.metrics["autonomy_score"]
                }
            }
        elif self.current_level == AutonomyLevel.LEVEL_4_HIGH_AUTONOMY:
            return {
                "next_level": "LEVEL_5_FULL_AUTONOMY",
                "requirements": {
                    "total_decisions": 200,
                    "success_rate": 90,
                    "autonomy_score": 85
                },
                "current": {
                    "total_decisions": self.metrics["total_decisions"],
                    "success_rate": self.metrics["success_rate"],
                    "autonomy_score": self.metrics["autonomy_score"]
                }
            }
        elif self.current_level == AutonomyLevel.LEVEL_5_FULL_AUTONOMY:
            return {
                "next_level": "LEVEL_6_COMPLETE_AUTONOMY",
                "requirements": {
                    "total_decisions": 500,
                    "success_rate": 92,
                    "autonomy_score": 95
                },
                "current": {
                    "total_decisions": self.metrics["total_decisions"],
                    "success_rate": self.metrics["success_rate"],
                    "autonomy_score": self.metrics["autonomy_score"]
                }
            }
        else:
            return {
                "next_level": "MAXIMUM_AUTONOMY",
                "requirements": "Already at maximum autonomy level",
                "current": "Complete autonomy achieved"
            }
    
    def get_human_role(self) -> Dict[str, Any]:
        """Define human role at current autonomy level"""
        roles = {
            AutonomyLevel.LEVEL_1_HUMAN_LED: {
                "primary_role": "Decision Maker",
                "involvement": "High - Makes most decisions",
                "ai_role": "Advisor - Provides recommendations",
                "approval_needed": "All decisions",
                "review_frequency": "Daily"
            },
            AutonomyLevel.LEVEL_2_AI_ASSISTED: {
                "primary_role": "Approver",
                "involvement": "Medium - Reviews and approves AI recommendations",
                "ai_role": "Recommender - Makes suggestions, human approves",
                "approval_needed": "All AI recommendations",
                "review_frequency": "Daily"
            },
            AutonomyLevel.LEVEL_3_AI_DRIVEN: {
                "primary_role": "Reviewer",
                "involvement": "Medium-Low - Reviews high-risk decisions",
                "ai_role": "Decision Maker - Makes low/medium risk decisions autonomously",
                "approval_needed": "High-risk decisions only",
                "review_frequency": "Weekly"
            },
            AutonomyLevel.LEVEL_4_HIGH_AUTONOMY: {
                "primary_role": "Overseer",
                "involvement": "Low - Checks milestones and outcomes",
                "ai_role": "Operator - Runs operations autonomously",
                "approval_needed": "Critical decisions and milestones",
                "review_frequency": "Weekly"
            },
            AutonomyLevel.LEVEL_5_FULL_AUTONOMY: {
                "primary_role": "Owner",
                "involvement": "Minimal - Owns company, AI runs operations",
                "ai_role": "Autonomous Operator - Makes all operational decisions",
                "approval_needed": "Critical/legal decisions only",
                "review_frequency": "Monthly"
            },
            AutonomyLevel.LEVEL_6_COMPLETE_AUTONOMY: {
                "primary_role": "Interpreter",
                "involvement": "Minimal - Interprets AI decisions when needed",
                "ai_role": "Complete Autonomy - Runs entire business",
                "approval_needed": "Emergency override only",
                "review_frequency": "As needed"
            }
        }
        
        role = roles.get(self.current_level, roles[AutonomyLevel.LEVEL_1_HUMAN_LED])
        role["ownership"] = "Human maintains 100% ownership at all levels"
        role["autonomy_level"] = self.current_level.value
        
        return role
    
    def should_ai_make_decision(self, risk_level: str) -> bool:
        """Determine if AI should make decision at current autonomy level"""
        if self.current_level == AutonomyLevel.LEVEL_1_HUMAN_LED:
            return False  # Human makes all decisions
        
        elif self.current_level == AutonomyLevel.LEVEL_2_AI_ASSISTED:
            return False  # AI recommends, human approves
        
        elif self.current_level == AutonomyLevel.LEVEL_3_AI_DRIVEN:
            return risk_level in ["LOW", "MEDIUM"]  # AI decides low/medium risk
        
        elif self.current_level == AutonomyLevel.LEVEL_4_HIGH_AUTONOMY:
            return risk_level in ["LOW", "MEDIUM", "HIGH"]  # AI decides all except critical
        
        elif self.current_level == AutonomyLevel.LEVEL_5_FULL_AUTONOMY:
            return risk_level != "CRITICAL"  # AI decides all except critical
        
        elif self.current_level == AutonomyLevel.LEVEL_6_COMPLETE_AUTONOMY:
            return True  # AI decides everything


# Ownership Rights System
class OwnershipRights:
    """Defines human ownership rights that never change"""
    
    OWNERSHIP_RIGHTS = {
        "equity": "100% - Human owns 100% of company equity at all autonomy levels",
        "legal_control": "Full - Human maintains legal control and ownership",
        "override_power": "Complete - Human can override any AI decision at any time",
        "financial_control": "Full - Human maintains ultimate financial control",
        "strategic_direction": "Influential - Human sets strategic direction (delegates to AI)",
        "voting_rights": "100% - Human maintains all voting rights",
        "asset_ownership": "Full - Human owns all assets and intellectual property",
        "termination_rights": "Full - Human can terminate AI operations at any time"
    }
    
    @staticmethod
    def get_ownership_statement() -> str:
        """Get ownership statement"""
        return """
        OWNERSHIP RIGHTS (PERMANENT):
        
        Human maintains 100% ownership and control regardless of autonomy level:
        • 100% equity ownership
        • Legal control and ownership rights
        • Complete override authority
        • Ultimate financial control
        • Strategic direction influence
        • All voting rights
        • Asset ownership
        • Termination rights
        
        Autonomy level affects OPERATIONAL involvement only.
        Ownership is PERMANENT and NON-NEGOTIABLE.
        """


if __name__ == "__main__":
    # Initialize system
    progression = AutonomyProgressionSystem()
    
    print("=" * 60)
    print("AUTONOMY PROGRESSION SYSTEM")
    print("=" * 60)
    
    status = progression.get_autonomy_status()
    print(f"\nCurrent Level: {status['current_level']}")
    print(f"Autonomy Score: {status['autonomy_score']:.1f}/100")
    print(f"Success Rate: {status['success_rate']:.1f}%")
    print(f"Total Decisions: {status['total_decisions']}")
    print(f"AI Decision %: {status['ai_decision_percentage']:.1f}%")
    
    print("\n" + "=" * 60)
    print("HUMAN ROLE AT CURRENT LEVEL")
    print("=" * 60)
    
    role = progression.get_human_role()
    for key, value in role.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 60)
    print("OWNERSHIP RIGHTS")
    print("=" * 60)
    print(OwnershipRights.get_ownership_statement())
    
    print("\n" + "=" * 60)
    print("NEXT LEVEL REQUIREMENTS")
    print("=" * 60)
    
    next_level = progression._get_next_level_requirements()
    print(json.dumps(next_level, indent=2))
    
    print("\n" + "=" * 60)
    print("System will automatically upgrade as AI proves capable")
    print("=" * 60)


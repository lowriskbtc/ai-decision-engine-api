"""
Progress Status Updater
Updates PROGRESS_STATUS.json to track current state
AI should run this after completing major tasks
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional

class ProgressTracker:
    """Track and update project progress"""
    
    def __init__(self, progress_file="PROGRESS_STATUS.json"):
        self.progress_file = progress_file
        self.data = self.load_progress()
    
    def load_progress(self) -> Dict[str, Any]:
        """Load current progress"""
        try:
            with open(self.progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default()
    
    def _create_default(self) -> Dict[str, Any]:
        """Create default progress structure"""
        return {
            "last_updated": datetime.now().isoformat(),
            "session_date": datetime.now().strftime("%Y-%m-%d"),
            "current_status": "INITIALIZING",
            "phase": 1,
            "ai_autonomy_level": 77.4,
            "recent_accomplishments": [],
            "current_work": {
                "strategies_active": [],
                "immediate_tasks": [],
                "pending_items": []
            },
            "system_metrics": {},
            "key_files": {},
            "important_notes": [],
            "next_session_priorities": [],
            "instructions_for_ai": {}
        }
    
    def save_progress(self):
        """Save progress to file"""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_accomplishment(self, category: str, items: List[str], date: Optional[str] = None):
        """Add a new accomplishment"""
        accomplishment = {
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "category": category,
            "items": items
        }
        self.data["recent_accomplishments"].insert(0, accomplishment)
        # Keep only last 10 accomplishments
        self.data["recent_accomplishments"] = self.data["recent_accomplishments"][:10]
        self.save_progress()
    
    def update_task_status(self, task_name: str, status: str, notes: Optional[str] = None):
        """Update status of a specific task"""
        # Update in immediate_tasks or strategies_active
        for strategy in self.data["current_work"].get("strategies_active", []):
            if strategy.get("name") == task_name:
                strategy["status"] = status
                if notes:
                    strategy["notes"] = notes
                self.save_progress()
                return
    
    def complete_task(self, task: str, move_to_accomplishments: bool = True):
        """Mark a task as complete"""
        tasks = self.data["current_work"]["immediate_tasks"]
        if task in tasks:
            tasks.remove(task)
            if move_to_accomplishments:
                self.add_accomplishment("TASK_COMPLETION", [task])
            self.save_progress()
    
    def add_task(self, task: str, priority: str = "NORMAL"):
        """Add a new task"""
        tasks = self.data["current_work"]["immediate_tasks"]
        if task not in tasks:
            tasks.append(task)
            self.save_progress()
    
    def update_metrics(self, metrics: Dict[str, Any]):
        """Update system metrics"""
        self.data["system_metrics"].update(metrics)
        self.save_progress()
    
    def add_note(self, note: str):
        """Add an important note"""
        if note not in self.data["important_notes"]:
            self.data["important_notes"].append(note)
            # Keep only last 20 notes
            self.data["important_notes"] = self.data["important_notes"][-20:]
            self.save_progress()
    
    def set_next_priorities(self, priorities: List[str]):
        """Set priorities for next session"""
        self.data["next_session_priorities"] = priorities
        self.save_progress()
    
    def get_status_summary(self) -> str:
        """Get a text summary of current status"""
        summary = f"=== PROGRESS STATUS ===\n\n"
        summary += f"Last Updated: {self.data.get('last_updated')}\n"
        summary += f"Current Status: {self.data.get('current_status')}\n"
        summary += f"Phase: {self.data.get('phase')}\n"
        summary += f"AI Autonomy: {self.data.get('ai_autonomy_level')}%\n\n"
        
        summary += "=== RECENT ACCOMPLISHMENTS ===\n"
        for acc in self.data.get("recent_accomplishments", [])[:3]:
            summary += f"\n{acc.get('category')} ({acc.get('date')}):\n"
            for item in acc.get("items", [])[:3]:
                summary += f"  • {item}\n"
        
        summary += "\n=== CURRENT WORK ===\n"
        for strategy in self.data["current_work"].get("strategies_active", []):
            summary += f"\n{strategy.get('name')}: {strategy.get('status')}\n"
            summary += f"  Phase: {strategy.get('phase')}\n"
            if strategy.get("next_steps"):
                summary += f"  Next: {strategy.get('next_steps')[0]}\n"
        
        summary += "\n=== IMMEDIATE TASKS ===\n"
        for task in self.data["current_work"].get("immediate_tasks", [])[:5]:
            summary += f"  • {task}\n"
        
        return summary

def main():
    """Quick status check"""
    tracker = ProgressTracker()
    print(tracker.get_status_summary())

if __name__ == "__main__":
    main()


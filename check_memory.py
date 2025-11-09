"""
Quick Memory Check
Shows what the AI remembers
"""

from ai_memory_system import AIMemory
import json

def show_memory():
    memory = AIMemory()
    
    print("=" * 60)
    print("AI MEMORY STATUS")
    print("=" * 60)
    
    summary = memory.get_memory_summary()
    print(f"\nTotal Events: {summary['total_events']}")
    print(f"Total Decisions: {summary['total_decisions']}")
    print(f"Total Outcomes: {summary['total_outcomes']}")
    print(f"Total Learnings: {summary['total_learnings']}")
    print(f"Successful Decisions: {summary['successful_decisions']}")
    print(f"Recent Activity (24h): {summary['recent_activity']}")
    
    print("\n" + "=" * 60)
    print("RECENT EVENTS")
    print("=" * 60)
    
    recent = memory.get_recent_activity(24)
    for event in recent[-10:]:  # Last 10 events
        print(f"\n[{event['timestamp']}] {event['type']}: {event['description']}")
        if event.get('data'):
            print(f"  Data: {json.dumps(event['data'], indent=2)}")
    
    print("\n" + "=" * 60)
    print("MEMORY FILE: ai_memory.json")
    print("=" * 60)
    print("\nAI uses this memory to:")
    print("• Inform future decisions")
    print("• Learn from outcomes")
    print("• Recognize patterns")
    print("• React based on past experiences")

if __name__ == "__main__":
    show_memory()


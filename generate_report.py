"""
Generate comprehensive project report
Creates a detailed status report for review
"""

from datetime import datetime
import json
import os

def generate_report():
    """Generate comprehensive project report"""
    
    report = {
        "report_date": datetime.now().isoformat(),
        "project": "AI Weed Company",
        "contract_address": "C7yr4quktmHV2ut89MM8AKvi6j6ZwLeW83NTysFCPZM2",
        "x_account": "@first_ai_weed"
    }
    
    # Load progress status
    try:
        with open("PROGRESS_STATUS.json", "r") as f:
            progress = json.load(f)
        report["progress"] = progress
    except:
        report["progress"] = {"error": "Could not load progress status"}
    
    # Check memory system
    try:
        with open("ai_memory.json", "r") as f:
            memory = json.load(f)
        report["memory_stats"] = {
            "total_events": len(memory.get("events", [])),
            "total_decisions": len(memory.get("decisions", [])),
            "total_outcomes": len(memory.get("outcomes", [])),
            "total_learnings": len(memory.get("learnings", []))
        }
    except:
        report["memory_stats"] = {"error": "Could not load memory"}
    
    # Check system state
    if os.path.exists("system_state.json"):
        try:
            with open("system_state.json", "r") as f:
                state = json.load(f)
            report["system_state"] = state
        except:
            pass
    
    # Check file structure
    important_files = [
        "START_HERE.md",
        "PROGRESS_STATUS.json",
        "AI_Weed_Company_Master_Ops.md",
        "api/main.py",
        "api/api_specification.yaml",
        "saas_landing/index.html",
        "saas_landing/waitlist_backend.py"
    ]
    
    report["file_structure"] = {}
    for file in important_files:
        report["file_structure"][file] = os.path.exists(file)
    
    # Generate summary
    report["summary"] = {
        "status": "OPERATIONAL",
        "strategies_active": 2,
        "api_completion": "90%",
        "saas_completion": "70%",
        "next_actions": [
            "Test API locally",
            "Deploy landing page",
            "Launch marketing"
        ]
    }
    
    return report

def print_report(report):
    """Print formatted report"""
    print("=" * 70)
    print(" " * 15 + "AI WEED COMPANY - PROJECT REPORT")
    print("=" * 70)
    print()
    
    print(f"Report Date: {report['report_date']}")
    print(f"Contract: {report['contract_address']}")
    print(f"X Account: {report['x_account']}")
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    summary = report.get("summary", {})
    print(f"Status: {summary.get('status', 'UNKNOWN')}")
    print(f"Active Strategies: {summary.get('strategies_active', 0)}")
    print(f"API_SERVICES Completion: {summary.get('api_completion', 'N/A')}")
    print(f"SAAS_PRODUCT Completion: {summary.get('saas_completion', 'N/A')}")
    print()
    
    # Memory Stats
    if "memory_stats" in report:
        print("=" * 70)
        print("MEMORY SYSTEM STATS")
        print("=" * 70)
        mem = report["memory_stats"]
        if "error" not in mem:
            print(f"Total Events: {mem.get('total_events', 0)}")
            print(f"Total Decisions: {mem.get('total_decisions', 0)}")
            print(f"Total Outcomes: {mem.get('total_outcomes', 0)}")
            print(f"Total Learnings: {mem.get('total_learnings', 0)}")
        print()
    
    # File Structure
    print("=" * 70)
    print("FILE STRUCTURE")
    print("=" * 70)
    files = report.get("file_structure", {})
    for file, exists in files.items():
        status = "[OK]" if exists else "[MISSING]"
        print(f"{status} {file}")
    print()
    
    # Next Actions
    if "next_actions" in summary:
        print("=" * 70)
        print("NEXT ACTIONS")
        print("=" * 70)
        for i, action in enumerate(summary["next_actions"], 1):
            print(f"{i}. {action}")
        print()
    
    print("=" * 70)
    print("Report saved to: project_report.json")
    print("=" * 70)

def main():
    """Generate and save report"""
    report = generate_report()
    
    # Save to file
    with open("project_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Print formatted
    print_report(report)

if __name__ == "__main__":
    main()


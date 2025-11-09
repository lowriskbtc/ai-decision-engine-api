"""
Project Health Checker
Comprehensive project health and readiness check
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class ProjectHealthChecker:
    """Check overall project health"""
    
    def __init__(self):
        self.project_root = Path(".")
        self.checks = []
        self.issues = []
    
    def check_python_version(self) -> bool:
        """Check Python version"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            self.checks.append(("Python Version", "PASS", f"{version.major}.{version.minor}.{version.micro}"))
            return True
        else:
            self.checks.append(("Python Version", "FAIL", f"{version.major}.{version.minor} (Need 3.8+)"))
            self.issues.append("Python version too old")
            return False
    
    def check_dependencies(self) -> bool:
        """Check if dependencies are installed"""
        try:
            import fastapi
            import uvicorn
            self.checks.append(("Dependencies", "PASS", "Installed"))
            return True
        except ImportError:
            self.checks.append(("Dependencies", "FAIL", "Missing"))
            self.issues.append("Dependencies not installed")
            return False
    
    def check_files(self) -> bool:
        """Check required files exist"""
        required = [
            "api/main.py",
            "api/requirements.txt",
            "README.md",
            "CHANGELOG.md"
        ]
        
        missing = []
        for file in required:
            if (self.project_root / file).exists():
                self.checks.append((f"File: {file}", "PASS", "Exists"))
            else:
                self.checks.append((f"File: {file}", "FAIL", "Missing"))
                missing.append(file)
        
        if missing:
            self.issues.append(f"Missing files: {', '.join(missing)}")
            return False
        return True
    
    def check_api_server(self) -> bool:
        """Check if API server is running"""
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                self.checks.append(("API Server", "PASS", "Running"))
                return True
            else:
                self.checks.append(("API Server", "FAIL", f"Status: {response.status_code}"))
                return False
        except:
            self.checks.append(("API Server", "WARN", "Not running (optional)"))
            return True  # Not critical
    
    def check_tests(self) -> bool:
        """Check if tests can run"""
        test_file = self.project_root / "api" / "test_api.py"
        if test_file.exists():
            self.checks.append(("Tests", "PASS", "Test file exists"))
            return True
        else:
            self.checks.append(("Tests", "WARN", "Test file not found"))
            return True
    
    def check_documentation(self) -> bool:
        """Check documentation completeness"""
        docs = [
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "OPERATIONAL_RUNBOOK.md"
        ]
        
        found = sum(1 for doc in docs if (self.project_root / doc).exists())
        self.checks.append(("Documentation", "PASS" if found >= 3 else "WARN", f"{found}/{len(docs)} files"))
        return found >= 3
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate health report"""
        # Run all checks
        self.check_python_version()
        self.check_dependencies()
        self.check_files()
        self.check_api_server()
        self.check_tests()
        self.check_documentation()
        
        # Calculate health score
        passed = sum(1 for _, status, _ in self.checks if status == "PASS")
        total = len(self.checks)
        health_score = (passed / total * 100) if total > 0 else 0
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "health_score": round(health_score, 2),
            "checks": [
                {"name": name, "status": status, "details": details}
                for name, status, details in self.checks
            ],
            "issues": self.issues,
            "status": "healthy" if health_score >= 80 else "needs_attention"
        }
        
        return report
    
    def print_report(self, report: Dict[str, Any]):
        """Print health report"""
        print("="*60)
        print("PROJECT HEALTH CHECK")
        print("="*60)
        print()
        print(f"Health Score: {report['health_score']}%")
        print(f"Status: {report['status'].upper()}")
        print()
        print("Checks:")
        for check in report['checks']:
            status_icon = {
                "PASS": "[OK]",
                "FAIL": "[FAIL]",
                "WARN": "[WARN]"
            }.get(check['status'], "[?]")
            print(f"  {status_icon} {check['name']}: {check['details']}")
        
        if report['issues']:
            print()
            print("Issues:")
            for issue in report['issues']:
                print(f"  - {issue}")
        
        print()

def main():
    """Run health check"""
    checker = ProjectHealthChecker()
    report = checker.generate_report()
    checker.print_report(report)
    
    # Save report
    with open("project_health_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to: project_health_report.json")

if __name__ == "__main__":
    main()


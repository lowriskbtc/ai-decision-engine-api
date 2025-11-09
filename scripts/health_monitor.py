"""
Health Monitor
Continuous health monitoring for the API
"""

import requests
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class HealthMonitor:
    """Monitor API health"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.health_log_file = "health_monitor.log"
        self.health_data_file = "health_data.json"
        self.check_interval = 60  # seconds
    
    def check_health(self) -> Dict:
        """Check API health"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.api_url}/health", timeout=5)
            response_time = (time.time() - start_time) * 1000  # ms
            
            is_healthy = response.status_code == 200
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "status": "healthy" if is_healthy else "unhealthy",
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "url": self.api_url
            }
            
            if is_healthy:
                try:
                    data = response.json()
                    result.update(data)
                except:
                    pass
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e),
                "url": self.api_url
            }
    
    def log_health(self, result: Dict):
        """Log health check result"""
        # Log to file
        log_entry = f"{result['timestamp']} - {result['status']} - {result.get('response_time_ms', 'N/A')}ms\n"
        with open(self.health_log_file, "a") as f:
            f.write(log_entry)
        
        # Save to JSON
        try:
            with open(self.health_data_file, "r") as f:
                data = json.load(f)
        except:
            data = {"checks": []}
        
        data["checks"].append(result)
        
        # Keep only last 1000 checks
        if len(data["checks"]) > 1000:
            data["checks"] = data["checks"][-1000:]
        
        with open(self.health_data_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def monitor_continuous(self):
        """Monitor continuously"""
        print(f"Starting health monitor for {self.api_url}")
        print(f"Check interval: {self.check_interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                result = self.check_health()
                self.log_health(result)
                
                status_icon = "✓" if result["status"] == "healthy" else "✗"
                print(f"{status_icon} {result['timestamp']} - {result['status']} - {result.get('response_time_ms', 'N/A')}ms")
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped")
    
    def get_stats(self) -> Dict:
        """Get health statistics"""
        try:
            with open(self.health_data_file, "r") as f:
                data = json.load(f)
        except:
            return {"error": "No data available"}
        
        checks = data.get("checks", [])
        if not checks:
            return {"error": "No checks available"}
        
        healthy_count = sum(1 for c in checks if c.get("status") == "healthy")
        total_count = len(checks)
        
        response_times = [c.get("response_time_ms", 0) for c in checks if "response_time_ms" in c]
        
        stats = {
            "total_checks": total_count,
            "healthy_checks": healthy_count,
            "unhealthy_checks": total_count - healthy_count,
            "uptime_percentage": round((healthy_count / total_count) * 100,  # Simplified
            "average_response_time_ms": round(sum(response_times) / len(response_times), 2) if response_times else 0,
            "min_response_time_ms": min(response_times) if response_times else 0,
            "max_response_time_ms": max(response_times) if response_times else 0
        }
        
        return stats

def main():
    """Run health monitor"""
    import sys
    
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    monitor = HealthMonitor(api_url)
    
    if len(sys.argv) > 2 and sys.argv[2] == "stats":
        stats = monitor.get_stats()
        print("\nHealth Statistics:")
        print(json.dumps(stats, indent=2))
    else:
        monitor.monitor_continuous()

if __name__ == "__main__":
    main()


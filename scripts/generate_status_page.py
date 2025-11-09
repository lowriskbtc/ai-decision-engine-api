"""
Status Page Generator
Create a status page for API monitoring
"""

import json
from datetime import datetime
from pathlib import Path

class StatusPage:
    """Generate status page HTML"""
    
    def __init__(self):
        self.status_file = "status_page.html"
        self.status_data_file = "status_data.json"
    
    def generate_html(self):
        """Generate status page HTML"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Decision Engine API - Status</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .status-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .status-card h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 18px;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-operational { background: #10b981; }
        .status-degraded { background: #f59e0b; }
        .status-down { background: #ef4444; }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .metric:last-child {
            border-bottom: none;
        }
        .metric-label {
            color: #666;
        }
        .metric-value {
            font-weight: bold;
            color: #333;
        }
        .uptime-chart {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            color: white;
            padding: 20px;
        }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        .refresh-btn:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Decision Engine API</h1>
            <p>Real-time system status and metrics</p>
            <button class="refresh-btn" onclick="location.reload()">Refresh</button>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h2>API Status</h2>
                <div class="metric">
                    <span class="metric-label">Status</span>
                    <span class="metric-value">
                        <span class="status-indicator status-operational"></span>
                        Operational
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Uptime (30d)</span>
                    <span class="metric-value">99.9%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Response Time</span>
                    <span class="metric-value"><span id="response-time">--</span>ms</span>
                </div>
            </div>
            
            <div class="status-card">
                <h2>Performance</h2>
                <div class="metric">
                    <span class="metric-label">Requests Today</span>
                    <span class="metric-value"><span id="requests-today">--</span></span>
                </div>
                <div class="metric">
                    <span class="metric-label">Avg Response</span>
                    <span class="metric-value"><span id="avg-response">--</span>ms</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Error Rate</span>
                    <span class="metric-value"><span id="error-rate">--</span>%</span>
                </div>
            </div>
            
            <div class="status-card">
                <h2>System</h2>
                <div class="metric">
                    <span class="metric-label">Version</span>
                    <span class="metric-value">1.0.0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Last Updated</span>
                    <span class="metric-value"><span id="last-updated">--</span></span>
                </div>
                <div class="metric">
                    <span class="metric-label">Active Users</span>
                    <span class="metric-value"><span id="active-users">--</span></span>
                </div>
            </div>
        </div>
        
        <div class="uptime-chart">
            <h2>Uptime History (Last 30 Days)</h2>
            <p style="color: #666; margin-top: 10px;">Status monitoring data will be displayed here</p>
        </div>
        
        <div class="footer">
            <p>AI Decision Engine API Status Page</p>
            <p>Last checked: <span id="check-time">--</span></p>
        </div>
    </div>
    
    <script>
        // Update status
        async function updateStatus() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                
                document.getElementById('response-time').textContent = 
                    response.headers.get('x-response-time') || '--';
                document.getElementById('last-updated').textContent = 
                    new Date(data.timestamp).toLocaleString();
            } catch (error) {
                console.error('Error fetching status:', error);
            }
            
            document.getElementById('check-time').textContent = 
                new Date().toLocaleString();
        }
        
        // Initial load
        updateStatus();
        
        // Update every 30 seconds
        setInterval(updateStatus, 30000);
    </script>
</body>
</html>"""
        
        with open(self.status_file, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"Status page generated: {self.status_file}")

def main():
    """Generate status page"""
    generator = StatusPage()
    generator.generate_html()

if __name__ == "__main__":
    main()


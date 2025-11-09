"""
API Key Management System
Handles API key generation, validation, and rate limiting
"""

import hashlib
import secrets
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

API_KEYS_FILE = os.getenv("API_KEYS_FILE", "api_keys.json")
RATE_LIMIT_FILE = os.getenv("RATE_LIMIT_FILE", "rate_limits.json")

class APIKeyManager:
    """Manage API keys and authentication"""
    
    def __init__(self):
        self.keys_file = API_KEYS_FILE
        self.rate_limit_file = RATE_LIMIT_FILE
        self._ensure_files_exist()
        self._load_keys()
    
    def _ensure_files_exist(self):
        """Ensure API keys file exists"""
        if not os.path.exists(self.keys_file):
            # Create default keys for development
            default_keys = {
                "dev_key_123": {
                    "tier": "dev",
                    "requests_per_month": 1000,
                    "created_at": datetime.now().isoformat(),
                    "active": True
                },
                "pro_key_456": {
                    "tier": "pro",
                    "requests_per_month": 10000,
                    "created_at": datetime.now().isoformat(),
                    "active": True
                }
            }
            self._save_keys(default_keys)
    
    def _load_keys(self) -> Dict[str, Any]:
        """Load API keys from file"""
        try:
            with open(self.keys_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def _save_keys(self, keys: Dict[str, Any]):
        """Save API keys to file"""
        with open(self.keys_file, "w") as f:
            json.dump(keys, f, indent=2)
    
    def generate_api_key(self, tier: str = "free", prefix: str = "key") -> str:
        """
        Generate a new API key
        
        Args:
            tier: API tier (free, pro, enterprise)
            prefix: Key prefix
        
        Returns:
            Generated API key
        """
        # Generate secure random key
        random_part = secrets.token_urlsafe(32)
        api_key = f"{prefix}_{random_part}"
        
        # Load existing keys
        keys = self._load_keys()
        
        # Add new key
        keys[api_key] = {
            "tier": tier,
            "requests_per_month": self._get_tier_limit(tier),
            "created_at": datetime.now().isoformat(),
            "active": True
        }
        
        # Save keys
        self._save_keys(keys)
        
        return api_key
    
    def _get_tier_limit(self, tier: str) -> int:
        """Get request limit for tier"""
        limits = {
            "free": 100,
            "dev": 1000,
            "pro": 10000,
            "enterprise": 1000000
        }
        return limits.get(tier.lower(), 100)
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Validate an API key
        
        Args:
            api_key: API key to validate
        
        Returns:
            Key info if valid, None otherwise
        """
        keys = self._load_keys()
        
        if api_key not in keys:
            return None
        
        key_info = keys[api_key]
        
        # Check if key is active
        if not key_info.get("active", False):
            return None
        
        # Check rate limits
        if not self._check_rate_limit(api_key, key_info):
            return None
        
        return key_info
    
    def _check_rate_limit(self, api_key: str, key_info: Dict[str, Any]) -> bool:
        """Check if API key is within rate limits"""
        try:
            with open(self.rate_limit_file, "r") as f:
                rate_limits = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            rate_limits = {}
        
        # Get current month key
        current_month = datetime.now().strftime("%Y-%m")
        month_key = f"{api_key}_{current_month}"
        
        # Get requests this month
        requests_this_month = rate_limits.get(month_key, {}).get("count", 0)
        max_requests = key_info.get("requests_per_month", 100)
        
        # Check if limit exceeded
        if requests_this_month >= max_requests:
            return False
        
        return True
    
    def record_request(self, api_key: str):
        """Record an API request for rate limiting"""
        try:
            with open(self.rate_limit_file, "r") as f:
                rate_limits = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            rate_limits = {}
        
        # Get current month key
        current_month = datetime.now().strftime("%Y-%m")
        month_key = f"{api_key}_{current_month}"
        
        # Initialize if needed
        if month_key not in rate_limits:
            rate_limits[month_key] = {
                "count": 0,
                "first_request": datetime.now().isoformat()
            }
        
        # Increment count
        rate_limits[month_key]["count"] = rate_limits[month_key].get("count", 0) + 1
        rate_limits[month_key]["last_request"] = datetime.now().isoformat()
        
        # Save
        with open(self.rate_limit_file, "w") as f:
            json.dump(rate_limits, f, indent=2)
    
    def get_key_info(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Get information about an API key"""
        keys = self._load_keys()
        return keys.get(api_key)
    
    def deactivate_key(self, api_key: str) -> bool:
        """Deactivate an API key"""
        keys = self._load_keys()
        if api_key in keys:
            keys[api_key]["active"] = False
            self._save_keys(keys)
            return True
        return False
    
    def list_keys(self) -> Dict[str, Any]:
        """List all API keys (admin function)"""
        return self._load_keys()

# Global instance
api_key_manager = APIKeyManager()


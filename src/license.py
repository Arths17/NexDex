# NexDex License System
# Handles feature gating for Community vs Enterprise editions

import os
import json
from typing import Dict, Any
from datetime import datetime, timedelta
from pathlib import Path


class License:
    """License management for NexDex editions"""
    
    COMMUNITY = "community"
    ENTERPRISE = "enterprise"
    
    def __init__(self, license_file: str = "license.json"):
        self.license_file = Path(license_file)
        self.edition = self.COMMUNITY
        self.features = self._get_default_features()
        self._load_license()
    
    def _get_default_features(self) -> Dict[str, bool]:
        """Get default feature flags for Community edition"""
        return {
            # Community Features (Always True)
            "basic_simulation": True,
            "scenario_management": True,
            "html_reports": True,
            "json_export": True,
            "csv_export": True,
            "web_dashboard": True,
            
            # Enterprise Features (Gated)
            "advanced_analytics": False,
            "custom_report_templates": False,
            "scheduled_simulations": False,
            "team_collaboration": False,
            "email_notifications": False,
            "dark_mode": False,
            "pdf_export": False,
            "api_access": False,
            "sso_authentication": False,
            "audit_logging": False,
            "custom_branding": False,
            "priority_support": False
        }
    
    def _load_license(self):
        """Load license from file if it exists"""
        if not self.license_file.exists():
            return
        
        try:
            with open(self.license_file, 'r') as f:
                license_data = json.load(f)
            
            # Validate license
            if self._validate_license(license_data):
                self.edition = license_data.get('edition', self.COMMUNITY)
                self.features.update(license_data.get('features', {}))
        except Exception as e:
            print(f"Warning: Could not load license: {e}")
    
    def _validate_license(self, license_data: Dict[str, Any]) -> bool:
        """Validate license data"""
        required_fields = ['edition', 'issued_to', 'issued_date']
        
        if not all(field in license_data for field in required_fields):
            return False
        
        # Check expiration
        if 'expiration_date' in license_data:
            expiration = datetime.fromisoformat(license_data['expiration_date'])
            if datetime.now() > expiration:
                print("License expired")
                return False
        
        return True
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        return self.features.get(feature, False)
    
    def get_edition(self) -> str:
        """Get current edition"""
        return self.edition
    
    def is_enterprise(self) -> bool:
        """Check if enterprise edition"""
        return self.edition == self.ENTERPRISE
    
    def get_enabled_features(self) -> Dict[str, bool]:
        """Get all enabled features"""
        return {k: v for k, v in self.features.items() if v}
    
    def generate_license_key(self, edition: str, issued_to: str, duration_days: int = 365) -> Dict[str, Any]:
        """Generate a new license key (Enterprise edition only)"""
        if edition == self.ENTERPRISE:
            issued_date = datetime.now()
            expiration_date = issued_date + timedelta(days=duration_days)
            
            license_data = {
                'edition': edition,
                'issued_to': issued_to,
                'issued_date': issued_date.isoformat(),
                'expiration_date': expiration_date.isoformat(),
                'features': {
                    **self._get_default_features(),
                    # Enable all enterprise features
                    "advanced_analytics": True,
                    "custom_report_templates": True,
                    "scheduled_simulations": True,
                    "team_collaboration": True,
                    "email_notifications": True,
                    "dark_mode": True,
                    "pdf_export": True,
                    "api_access": True,
                    "sso_authentication": True,
                    "audit_logging": True,
                    "custom_branding": True,
                    "priority_support": True
                }
            }
            
            return license_data
        
        return {}


# Global license instance
_license = None


def get_license() -> License:
    """Get global license instance"""
    global _license
    if _license is None:
        _license = License()
    return _license


def check_feature(feature: str) -> bool:
    """Quick helper to check if feature is enabled"""
    return get_license().is_feature_enabled(feature)

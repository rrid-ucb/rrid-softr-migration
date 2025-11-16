"""
Configuration manager for video annotation system.
"""

import json
from pathlib import Path
from typing import Dict, Optional

from .models import ModelDiscovery


class ConfigManager:
    """Manage configuration for the video annotation system."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            config_dir = Path.home() / '.video_annotation'
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / 'config.json'
        self.model_discovery = ModelDiscovery(self.config_dir / 'models.json')
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_config(self):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure(self, interactive: bool = True):
        """Run interactive configuration."""
        print("\n" + "=" * 60)
        print("Video Annotation System - Configuration")
        print("=" * 60)
        
        # Configure models
        print("\n[1/3] Configuring Models...")
        model_config = self.model_discovery.configure_models(interactive=interactive)
        self.config['models'] = model_config
        
        # Configure speed preferences
        print("\n[2/3] Configuring Speed Preferences...")
        if interactive:
            print("\nSpeed preferences (affects model selection):")
            print("  1. Fast - Prioritize speed over accuracy")
            print("  2. Balanced - Good balance (recommended)")
            print("  3. Accurate - Prioritize accuracy over speed")
            
            choice = input("\nSelect preference (1-3) [2]: ").strip() or "2"
            speed_map = {'1': 'fast', '2': 'balanced', '3': 'accurate'}
            speed_preference = speed_map.get(choice, 'balanced')
        else:
            speed_preference = 'balanced'
        
        self.config['speed_preference'] = speed_preference
        
        # Configure output settings
        print("\n[3/3] Configuring Output Settings...")
        if interactive:
            timestamp_outputs = input("Use timestamped output directories? (y/n) [y]: ").strip().lower() or 'y'
            self.config['timestamped_outputs'] = timestamp_outputs == 'y'
        else:
            self.config['timestamped_outputs'] = True
        
        self._save_config()
        print("\n✓ Configuration saved!")
        return self.config
    
    def get_model(self, task_type: str) -> Optional[dict]:
        """Get configured model for a task type."""
        return self.config.get('models', {}).get(task_type)
    
    def get_speed_preference(self) -> str:
        """Get configured speed preference."""
        return self.config.get('speed_preference', 'balanced')
    
    def is_configured(self) -> bool:
        """Check if system is configured."""
        return bool(self.config.get('models'))


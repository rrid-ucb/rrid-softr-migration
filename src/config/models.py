"""
Model discovery and selection for transcription, vision, and general LLM tasks.
"""

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


@dataclass
class ModelInfo:
    """Information about an available model."""
    provider: str  # 'openai', 'gemini', 'whisper'
    name: str
    task_type: str  # 'transcription', 'vision', 'general', 'thinking'
    speed_tier: str  # 'fast', 'balanced', 'accurate'
    cost_tier: str  # 'low', 'medium', 'high'
    description: str
    supports_vision: bool = False
    supports_audio: bool = False


class ModelDiscovery:
    """Discover and manage available models."""
    
    # Whisper models (local)
    WHISPER_MODELS = [
        ModelInfo('whisper', 'tiny', 'transcription', 'fast', 'low', 
                 'Fastest, least accurate', supports_audio=True),
        ModelInfo('whisper', 'base', 'transcription', 'balanced', 'low',
                 'Good balance of speed and accuracy', supports_audio=True),
        ModelInfo('whisper', 'small', 'transcription', 'balanced', 'low',
                 'Better accuracy, slightly slower', supports_audio=True),
        ModelInfo('whisper', 'medium', 'transcription', 'accurate', 'low',
                 'High accuracy, slower', supports_audio=True),
        ModelInfo('whisper', 'large', 'transcription', 'accurate', 'low',
                 'Best accuracy, slowest', supports_audio=True),
        ModelInfo('whisper', 'large-v3', 'transcription', 'accurate', 'low',
                 'Latest large model, best accuracy', supports_audio=True),
    ]
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / '.video_annotation_config.json'
        self.config = self._load_config()
        self._discover_available_models()
    
    def _load_config(self) -> dict:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_config(self):
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _discover_available_models(self):
        """Discover available models from APIs."""
        self.available_models = {
            'whisper': self.WHISPER_MODELS,
            'openai': [],
            'gemini': [],
        }
        
        # Discover OpenAI models
        if OpenAI and os.getenv('OPENAI_API_KEY'):
            try:
                client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                models = client.models.list()
                
                # Filter and categorize OpenAI models
                for model in models:
                    model_id = model.id.lower()
                    if 'gpt-4' in model_id or 'o1' in model_id:
                        if 'vision' in model_id or 'o1' in model_id:
                            continue  # Handle separately
                        
                        if 'turbo' in model_id or 'o1-mini' in model_id:
                            speed = 'fast'
                        elif 'o1' in model_id:
                            speed = 'balanced'
                        else:
                            speed = 'accurate'
                        
                        task_type = 'thinking' if 'o1' in model_id else 'general'
                        
                        self.available_models['openai'].append(
                            ModelInfo('openai', model.id, task_type, speed, 'high',
                                    f'OpenAI {model.id}', supports_vision=False)
                        )
                    
                    if 'gpt-4o' in model_id or 'gpt-4-vision' in model_id:
                        self.available_models['openai'].append(
                            ModelInfo('openai', model.id, 'vision', 'balanced', 'high',
                                    f'OpenAI vision model {model.id}', supports_vision=True)
                        )
            except Exception as e:
                print(f"Warning: Could not discover OpenAI models: {e}", file=sys.stderr)
        
        # Discover Gemini models
        if genai and os.getenv('GEMINI_API_KEY'):
            try:
                genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
                
                # Known Gemini models (API doesn't always provide list_models easily)
                known_models = [
                    ('gemini-2.0-flash-exp', 'vision', 'fast', True),
                    ('gemini-1.5-flash', 'vision', 'fast', True),
                    ('gemini-1.5-pro', 'vision', 'accurate', True),
                    ('gemini-pro', 'general', 'balanced', False),
                ]
                
                for model_name, task_type, speed, supports_vision in known_models:
                    try:
                        # Try to create model to verify it exists
                        test_model = genai.GenerativeModel(model_name)
                        self.available_models['gemini'].append(
                            ModelInfo('gemini', model_name, task_type, speed, 'medium',
                                    f'Gemini {model_name}', supports_vision=supports_vision)
                        )
                    except Exception:
                        # Model not available, skip
                        pass
            except Exception as e:
                print(f"Warning: Could not discover Gemini models: {e}", file=sys.stderr)
    
    def get_recommended_models(self, task_type: str, speed_preference: str = 'balanced') -> List[ModelInfo]:
        """Get recommended models for a task type and speed preference."""
        recommendations = []
        
        for provider, models in self.available_models.items():
            for model in models:
                if model.task_type == task_type:
                    if speed_preference == 'fast' and model.speed_tier in ['fast', 'balanced']:
                        recommendations.append(model)
                    elif speed_preference == 'balanced' and model.speed_tier == 'balanced':
                        recommendations.append(model)
                    elif speed_preference == 'accurate' and model.speed_tier in ['balanced', 'accurate']:
                        recommendations.append(model)
        
        # Sort by speed tier preference
        speed_order = {'fast': 0, 'balanced': 1, 'accurate': 2}
        recommendations.sort(key=lambda m: speed_order.get(m.speed_tier, 99))
        
        return recommendations
    
    def configure_models(self, interactive: bool = True) -> dict:
        """Configure model selection interactively or with defaults."""
        config = {
            'transcription': {},
            'vision': {},
            'general': {},
            'thinking': {},
        }
        
        if interactive:
            print("\n" + "=" * 60)
            print("Model Configuration")
            print("=" * 60)
            
            for task_type in ['transcription', 'vision', 'general', 'thinking']:
                print(f"\n{task_type.upper()} Models:")
                recommendations = self.get_recommended_models(task_type, 'balanced')
                
                if not recommendations:
                    print(f"  No models available for {task_type}")
                    continue
                
                for i, model in enumerate(recommendations[:5], 1):
                    print(f"  {i}. {model.provider.upper()} - {model.name}")
                    print(f"     Speed: {model.speed_tier}, Cost: {model.cost_tier}")
                    print(f"     {model.description}")
                
                choice = input(f"\nSelect {task_type} model (1-{min(5, len(recommendations))}) or press Enter for default: ").strip()
                
                if choice and choice.isdigit() and 1 <= int(choice) <= len(recommendations):
                    selected = recommendations[int(choice) - 1]
                    config[task_type] = {
                        'provider': selected.provider,
                        'name': selected.name,
                    }
                elif recommendations:
                    # Default to first recommendation
                    selected = recommendations[0]
                    config[task_type] = {
                        'provider': selected.provider,
                        'name': selected.name,
                    }
        else:
            # Use defaults
            for task_type in ['transcription', 'vision', 'general', 'thinking']:
                recommendations = self.get_recommended_models(task_type, 'balanced')
                if recommendations:
                    selected = recommendations[0]
                    config[task_type] = {
                        'provider': selected.provider,
                        'name': selected.name,
                    }
        
        self.config['models'] = config
        self._save_config()
        return config
    
    def get_model_config(self, task_type: str) -> Optional[dict]:
        """Get configured model for a task type."""
        return self.config.get('models', {}).get(task_type)
    
    def list_models(self, task_type: Optional[str] = None) -> Dict[str, List[ModelInfo]]:
        """List all available models, optionally filtered by task type."""
        if task_type:
            return {task_type: self.available_models.get(task_type, [])}
        return self.available_models


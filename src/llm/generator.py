"""
LLM-powered document generation with model management.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from ..config.manager import ConfigManager


class LLMDocumentGenerator:
    """Generate documentation using LLMs with configured models."""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        
        # Setup API clients
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        self.gemini_model = None
        self.openai_client = None
        
        if self.gemini_key and genai:
            genai.configure(api_key=self.gemini_key)
            vision_model = self.config.get_model('vision')
            if vision_model and vision_model.get('provider') == 'gemini':
                try:
                    self.gemini_model = genai.GenerativeModel(vision_model['name'])
                except Exception as e:
                    print(f"Warning: Could not initialize Gemini model: {e}", file=sys.stderr)
        
        if self.openai_key and OpenAI:
            try:
                self.openai_client = OpenAI(api_key=self.openai_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}", file=sys.stderr)
    
    def generate_documents(
        self,
        annotated_json_path: Path,
        frames_dir: Path,
        output_dir: Path,
        providers: Optional[List[str]] = None
    ):
        """
        Generate all document types using configured models.
        
        Args:
            annotated_json_path: Path to annotated.json
            frames_dir: Directory containing frames
            output_dir: Output directory for generated documents
            providers: Optional list of providers to use (defaults to configured)
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load annotated data
        with open(annotated_json_path) as f:
            data = json.load(f)
        
        # Determine which providers to use
        if providers is None:
            providers = []
            if self.gemini_model:
                providers.append('gemini')
            if self.openai_client:
                providers.append('openai')
        
        if not providers:
            print("Warning: No LLM providers available. Set GEMINI_API_KEY or OPENAI_API_KEY.")
            return
        
        print(f"\nGenerating documents with providers: {', '.join(providers)}")
        
        # Generate each document type
        for provider in providers:
            suffix = f"_{provider}" if len(providers) > 1 else ""
            
            # Linear walkthrough
            print(f"\n[{provider}] Generating linear walkthrough...")
            linear_content = self._generate_linear_walkthrough(data, frames_dir, provider)
            if linear_content:
                (output_dir / f"linear_walkthrough{suffix}.md").write_text(linear_content)
            
            # PRD document
            print(f"[{provider}] Generating PRD...")
            prd_content = self._generate_prd(data, frames_dir, provider)
            if prd_content:
                (output_dir / f"prd_document{suffix}.md").write_text(prd_content)
            
            # Personas
            print(f"[{provider}] Generating personas...")
            personas_content = self._generate_personas(data, frames_dir, provider)
            if personas_content:
                (output_dir / f"personas_stories{suffix}.md").write_text(personas_content)
        
        print(f"\n✓ Documents generated in: {output_dir}")
    
    def _generate_linear_walkthrough(self, data: dict, frames_dir: Path, provider: str) -> Optional[str]:
        """Generate linear walkthrough document."""
        # This would integrate the logic from llm_annotate.py
        # For now, return placeholder
        return "# Linear Walkthrough\n\n*Document generation not yet fully integrated.*"
    
    def _generate_prd(self, data: dict, frames_dir: Path, provider: str) -> Optional[str]:
        """Generate PRD document."""
        return "# PRD Document\n\n*Document generation not yet fully integrated.*"
    
    def _generate_personas(self, data: dict, frames_dir: Path, provider: str) -> Optional[str]:
        """Generate personas document."""
        return "# Personas and User Stories\n\n*Document generation not yet fully integrated.*"


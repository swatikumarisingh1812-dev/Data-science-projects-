"""
Configuration management for Image Generation Agent
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import json


class Config:
    """Configuration manager for the image generation agent."""
    
    # Default configuration
    DEFAULTS = {
        'backend': 'huggingface',
        'models': {
            'huggingface': 'stabilityai/stable-diffusion-2-1',
            'openai': 'dall-e-3',
            'stability': 'stable-diffusion-xl-1024-v1-0'
        },
        'generation': {
            'width': 512,
            'height': 512,
            'num_images': 1,
            'num_inference_steps': 50,
            'guidance_scale': 7.5
        },
        'output': {
            'directory': 'generated_images',
            'prefix': 'image',
            'format': 'png'
        }
    }
    
    # Alternative models for each backend
    AVAILABLE_MODELS = {
        'huggingface': [
            'stabilityai/stable-diffusion-2-1',
            'stabilityai/stable-diffusion-xl-base-1.0',
            'runwayml/stable-diffusion-v1-5',
            'CompVis/stable-diffusion-v1-4',
            'prompthero/openjourney',
            'dreamlike-art/dreamlike-photoreal-2.0'
        ],
        'openai': [
            'dall-e-3',
            'dall-e-2'
        ],
        'stability': [
            'stable-diffusion-xl-1024-v1-0',
            'stable-diffusion-v1-6'
        ]
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to JSON configuration file (optional)
        """
        self.config = self.DEFAULTS.copy()
        self.config_file = config_file or self._get_default_config_path()
        
        # Load from file if exists
        if Path(self.config_file).exists():
            self.load()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        return str(Path.home() / '.image_agent_config.json')
    
    def load(self, config_file: Optional[str] = None) -> None:
        """
        Load configuration from JSON file.
        
        Args:
            config_file: Path to configuration file
        """
        file_path = config_file or self.config_file
        
        try:
            with open(file_path, 'r') as f:
                user_config = json.load(f)
                self._merge_config(user_config)
            print(f"Configuration loaded from: {file_path}")
        except FileNotFoundError:
            print(f"Configuration file not found: {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
    
    def save(self, config_file: Optional[str] = None) -> None:
        """
        Save current configuration to JSON file.
        
        Args:
            config_file: Path to configuration file
        """
        file_path = config_file or self.config_file
        
        try:
            with open(file_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"Configuration saved to: {file_path}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """Merge user configuration with defaults."""
        for key, value in user_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'generation.width')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_api_key(self, backend: str) -> Optional[str]:
        """
        Get API key for specified backend from environment variables.
        
        Args:
            backend: Backend name ('openai' or 'stability')
            
        Returns:
            API key or None
        """
        env_vars = {
            'openai': 'OPENAI_API_KEY',
            'stability': 'STABILITY_API_KEY'
        }
        
        env_var = env_vars.get(backend.lower())
        if env_var:
            return os.getenv(env_var)
        return None
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """
        Check which API keys are configured.
        
        Returns:
            Dictionary mapping backend names to availability status
        """
        return {
            'openai': bool(self.get_api_key('openai')),
            'stability': bool(self.get_api_key('stability')),
            'huggingface': True  # No API key required for local models
        }
    
    def get_model_for_backend(self, backend: str) -> str:
        """
        Get default model for specified backend.
        
        Args:
            backend: Backend name
            
        Returns:
            Model identifier
        """
        return self.config['models'].get(backend, '')
    
    def list_available_models(self, backend: str) -> list:
        """
        List available models for specified backend.
        
        Args:
            backend: Backend name
            
        Returns:
            List of model identifiers
        """
        return self.AVAILABLE_MODELS.get(backend, [])
    
    def print_config(self) -> None:
        """Print current configuration in a readable format."""
        print("\n=== Current Configuration ===")
        print(json.dumps(self.config, indent=2))
        print("\n=== API Key Status ===")
        api_status = self.validate_api_keys()
        for backend, available in api_status.items():
            status = "✓ Configured" if available else "✗ Not configured"
            print(f"{backend.capitalize()}: {status}")
        print()


def create_sample_config(output_path: str = 'image_agent_config.json') -> None:
    """
    Create a sample configuration file.
    
    Args:
        output_path: Path where to save the sample config
    """
    sample_config = {
        'backend': 'huggingface',
        'models': {
            'huggingface': 'stabilityai/stable-diffusion-2-1',
            'openai': 'dall-e-3',
            'stability': 'stable-diffusion-xl-1024-v1-0'
        },
        'generation': {
            'width': 768,
            'height': 768,
            'num_images': 1,
            'num_inference_steps': 50,
            'guidance_scale': 7.5,
            'negative_prompt': 'blurry, low quality, distorted'
        },
        'output': {
            'directory': 'generated_images',
            'prefix': 'ai_art',
            'format': 'png'
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print(f"Sample configuration created: {output_path}")
    print("\nTo use this configuration:")
    print("1. Edit the file with your preferences")
    print("2. Set API keys as environment variables:")
    print("   export OPENAI_API_KEY='your-key-here'")
    print("   export STABILITY_API_KEY='your-key-here'")


if __name__ == '__main__':
    # Demo usage
    config = Config()
    config.print_config()
    
    # Create sample config
    create_sample_config()
